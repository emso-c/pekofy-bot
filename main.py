import time
import random
from datetime import datetime
import argparse
import traceback
import logging
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler

import praw

from pekofy import pekofy
from auth import REDDIT, BOT_NAME, AUTHOR
from replies import REPLIES

logger = logging.getLogger(__name__)
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
handler = TimedRotatingFileHandler(filename='logs/pekolog.log', when='D', interval=1, backupCount=30, encoding='utf-8', delay=False)
formatter = Formatter(fmt=f"%(asctime)s:%(module)s[%(lineno)d]:%(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# for some reason it doesn't print the log output to the console if I delete this, help
logging.info(str)

SUBREDDIT_LIST = ['u_' + BOT_NAME, 'u_' + AUTHOR, 'hololive', 'VirtualYoutubers', 'Hololewd', 'okbuddyhololive',
                  'goodanimemes', 'VtuberV8', 'Priconne', 'AmeliaWatson', 'GawrGura']
SUBREDDIT = REDDIT.subreddit('+'.join(SUBREDDIT_LIST))

# used for exponential back off in case reddit server is unable to respond
INITIAL_WAIT_TIME = 5
MAX_WAIT_TIME = 600
RESET_LIMIT = 50

comments_replied, comments_scanned = 0, 0

def reply_f(reply, comment_obj, pekofy_msg=None, debug=False):
    """
    reply to a comment

    :param reply: the reply type to send
    :type reply: string
    :param comment_obj: the comment to reply
    :type comment_obj: praw.models.Comment
    :param pekofy_msg: pekofied message that should only be passed when the reply variable is 'pekofy' to
    pass the pekofied reply to the replies, defaults to None
    :type pekofy_msg: string
    :param debug: disable commenting and sending messages
    :type debug: bool
    """

    REPLIES["pekofy"]["messages"] = []
    if pekofy_msg:
        REPLIES["pekofy"]["messages"] = [pekofy_msg]
        if is_triggering(pekofy_msg, "nothing changed"):
            reply = "nothing changed"
    
    reply_content = REPLIES[reply]
    if not random.randint(0, 100) <= REPLIES[reply]['chance'] or \
            already_replied_to(comment_obj, reply):
        return

    message = random.choice(reply_content["messages"])
    try:
        if not debug:
            comment_obj.reply(message)
        global comments_replied
        comments_replied += 1
    except Exception:
        logger.error(f"Couldn't reply: {traceback.format_exc()}")
        if not debug:
            notify_author(traceback.format_exc(), comment_obj, message)
    logger.debug(f"{reply}: https://www.reddit.com{comment_obj.permalink}")
    logger.debug(f"Reply: {message}")


def already_replied_to(comment, reply_type):
    """ returns if already replied the same type of comment or not """
    
    second_refresh = False
    for _ in range(2):
      try:
          comment.refresh()
          break
      except praw.exceptions.ClientException: # work around as stated in the praw issue 838
          logger.error(f"Comments didn't load, trying again...")
          if second_refresh:
              logger.error("Couldn't load comments, assuming already replied")
              return True
          time.sleep(10)
          second_refresh = True
    comment.replies.replace_more()

    if reply_type == "pekofy":
        # pass pekofied reply to replies
        if is_top_level(comment):
            REPLIES[reply_type]["messages"] = [pekofy(
                comment.submission.title +
                '\n\n' +
                comment.submission.selftext if comment.submission.selftext else comment.submission.title)
            ]
        elif comment.parent():
            REPLIES[reply_type]["messages"] = [pekofy(comment.parent().body)]

    child_comments = comment.replies.list()
    for top_comment in child_comments:
        if top_comment.parent().id != comment.id:
            break
        if top_comment.author == BOT_NAME:
            if top_comment.body in REPLIES[reply_type]["messages"]:
                logger.warning(f"Already replied ({reply_type}): {top_comment.body}")
                logger.debug(f"https://www.reddit.com{top_comment.permalink}")
                return True
    return False


def notify_author(exception, comment=None, tried_reply=None):
    """ Notifies to the author, don't forget to whitelist the bot if your PM's are closed """

    title = datetime.now().strftime("%Y.%m.%d - %H:%M:%S")
    if comment and tried_reply:
        body = f"{BOT_NAME} has run into an error: {exception}\n" \
               f"Here\'s the [link](https://www.reddit.com{comment.permalink}) to the comment.\n" \
               f"Tried to reply this: {tried_reply}"
    else:
        body = f'{BOT_NAME} has run into an error: {exception}\n'
    try:
        REDDIT.redditor(AUTHOR).message(title, body)
        logger.info(f"Notified author")
    except Exception:
        logger.critical("Couldn't notify the author")


def is_triggering(text, reply):
    """ whether the text triggers the given reply type or not """

    if REPLIES[reply]['include_bot'] and not "bot" in text:
        return False

    trigger_expression = lambda trigger, text, exact: (trigger == text) if exact else (trigger in text)
    conditions = [
        trigger_expression(
            trigger, text, REPLIES[reply]["exact"]
        ) for trigger in REPLIES[reply]["triggers"]]

    condition = any(conditions)
    if REPLIES[reply]["trigger_type"] == "all":
        condition = all(conditions)

    if condition:
        logger.info(f"Trigger found ({reply}): {text}")
    return condition


def passed_limit(comment, limit=2):
    """ returns true if the same comment has been pekofied too much by
    climbing up the comment tree until it reaches the limit """

    current_usage = 0
    for _ in range(limit):
        if is_top_level(comment):
            break
        if comment.parent().author == BOT_NAME:
            comment = comment.parent()
            if is_top_level(comment):
                break
            if comment.parent().author and is_triggering(comment.parent().body, "pekofy"):
                comment = comment.parent()
                current_usage += 1
    if current_usage == limit:
        logger.warning(f"Reached limit ({limit}): https://www.reddit.com{comment.permalink} ({comment})")
    return current_usage == limit


def is_top_level(comment):
    """ returns if the comment is top level (directly replied to the post) """
    return comment.parent_id == comment.link_id


def is_anti(comment):
    """ Checks if author of the comment is a possible anti/hater by
        counting their overall comment score in the same comment tree """
    score_sum = comment.score
    temp_comment = comment

    if is_top_level(temp_comment):
        # should not enter here in any case
        return score_sum < -1

    while True:
        if is_top_level(temp_comment.parent()):
            break
        if temp_comment.parent().author:
            temp_comment = temp_comment.parent()
            if temp_comment.author == comment.author:  # same user in the comment chain, add to sum
                score_sum += temp_comment.score
        else:
            break
    
    if score_sum < -1:
        logger.info(f"Possible anti found: https://www.reddit.com{comment.permalink}, score was {score_sum}")
    return score_sum < -1

def is_between_timespan(timespan:tuple) -> bool:
    """Returns if current time is between given timespans"""
    return timespan[0] <= datetime.now() <= timespan[1]


def main(debug=False):
    global comments_replied, comments_scanned
    current_wait_time = INITIAL_WAIT_TIME

    logger.info(f"Debug mode is {'ON' if debug else 'OFF'}")

    # giving time to cancel in case accidentally running the program without debug option
    if not debug:
        for i in range(5, -1,-1):
            time.sleep(1)
            print(f"Starting in {i}...", end="\r")
        print(" "*20, end="\r")

    while True:
        try:
            # scan each comment
            for comment in SUBREDDIT.stream.comments():
                comments_scanned += 1

                # comment author is the bot itself
                if comment.author == BOT_NAME:
                    continue
                
                # comment has been deleted
                if not comment.author:
                    logger.warning(f"Comment has been deleted: https://www.reddit.com{comment.permalink}")
                    continue


                # check for pain peko reply
                if is_triggering(comment.body.lower(), "pain peko"):
                    reply_f("pain peko", comment, debug=debug)

                # check for hey moona reply
                if len(comment.body)<350:  # longer messages tend to be more serious, don't "hey moona"
                    if is_triggering(comment.body.lower(), "hey moona"):
                        reply_f("hey moona", comment, debug=debug)

                replied = False
                if not is_top_level(comment):
                    if comment.parent().author and comment.parent().author.name == BOT_NAME:
                        # limited time reply
                        CHRISTMAS=(
                            datetime(int(datetime.now().strftime("%Y")), 12, 25-1),
                            datetime(int(datetime.now().strftime("%Y"))+1, 1, 5+1)
                        )
                        if is_between_timespan(CHRISTMAS):
                            if is_triggering(comment.body.lower(), "merry christmas"):
                                reply_f("merry christmas", comment, debug=debug)
                                continue

                        # feedback gratitude
                        for feedback in ["love", "cute", "thank", "sorry", "insult"]:
                            if is_triggering(comment.body.lower(), feedback):
                                reply_f(feedback, comment, debug=debug)
                                replied = True
                                break
                if replied:
                    continue

                # both pekofy and unpekofy written
                if is_triggering(comment.body, "confused"):
                    reply_f("confused", comment, debug=debug)
                    continue

                # if keyword found, try to pekofy
                if is_triggering(comment.body, "pekofy"):

                    # can't pekofy due to comment not having any parent
                    if not comment.parent().author:
                        continue

                    # parent is a post, pekofy accordingly
                    if is_top_level(comment):
                        reply_f("pekofy", comment, debug=debug, pekofy_msg=pekofy(
                            comment.submission.title + '\n\n' + comment.submission.selftext if comment.submission.selftext else comment.submission.title))
                        continue

                    # someone tried to break it by recursive calling, kindly say no
                    if is_triggering(comment.parent().body, "pekofy"):
                        reply_f("no", comment, debug=debug)
                        continue

                    # someone tried to pekofy a good/bad bot reply, don't pekofy
                    if is_triggering(comment.parent().body.lower(), "bot score abuse"):
                        reply_f("bot score abuse", comment, debug=debug)
                        continue

                    # don't pekofy if limit already reached before.
                    if comment.parent().body == REPLIES["limit reached"]["messages"][0] and comment.parent().author == BOT_NAME:
                        continue

                    # if the same sentence has been pekofied too much already, don't pekofy
                    if passed_limit(comment):
                        reply_f("limit reached", comment, debug=debug)
                        continue

                    # not pekofy if anti/hater
                    if is_anti(comment):
                        reply_f("no", comment, debug=debug)
                        continue

                    # try to reply to the comment
                    reply_f("pekofy", comment, pekofy_msg=pekofy(comment.parent().body), debug=debug)

                # delete keyphrase found
                if is_triggering(comment.body, "unpekofy") and comment.parent().author == BOT_NAME and comment.parent().body:
                    if comment.parent().score < -1:
                        comment.parent().delete()
                        logger.info(f'Unpekofied: https://www.reddit.com{comment.parent().permalink}')
                        logger.info(f'Parent: https://www.reddit.com{comment.parent().parent().permalink}')

                # More than `reset_limit` comments has been scanned without an incident, reset wait time.
                if comments_scanned % RESET_LIMIT == 0:
                    current_wait_time = INITIAL_WAIT_TIME
        except KeyboardInterrupt:
            print("Keyboard Interrupt. Terminating...")
            break
        except praw.exceptions.RedditAPIException:
            logger.error(f"RedditAPIException: {traceback.format_exc()}")
            if not debug:
                notify_author(traceback.format_exc())
        except praw.exceptions.PRAWException:
            logger.error(f"PRAWException: {traceback.format_exc()}")
            if not debug:
                notify_author(traceback.format_exc())
        except Exception:
            logger.error(f"Unhandled exception: {traceback.format_exc()}")
            if not debug:
                notify_author(traceback.format_exc())
        finally:
            logger.info(f"Replied comments so far: {comments_replied}")
            logger.info(f"Scanned comments so far: {comments_scanned}")
            comments_replied, comments_scanned = 0, 0

            # not-so-exponential back off
            time.sleep(current_wait_time)
            if not current_wait_time > MAX_WAIT_TIME:
                logger.info(f"Increasing wait time from {current_wait_time} to {current_wait_time*2}")
                current_wait_time *= 2

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='turn debug mode on')
    args = parser.parse_args()

    logger.info("Starting session ----------------------------------------------------")
    main(debug=args.debug)