import praw
import string
from datetime import datetime
import time
import random
import credentials
import replies as r
import pekofy as peko  # because it sounds better

bot_name = credentials.bot_name
author = credentials.author
reddit = praw.Reddit(client_id=credentials.client_id,
                     client_secret=credentials.client_secret,
                     username=credentials.bot_name,
                     password=credentials.bot_pass,
                     user_agent=credentials.user_agent)
subreddit_list = ['u_' + bot_name, 'u_' + author, 'hololive', 'VirtualYoutubers', 'Hololewd', 'okbuddyhololive',
                  'goodanimemes', 'VtuberV8', 'Priconne', 'AmeliaWatson', 'GawrGura']
subreddit = reddit.subreddit('+'.join(subreddit_list))
replies = r.replies


def reply_f(reply, comment_obj, pekofy_msg=None):
    """
    reply to a comment

    :param reply: the reply type to send
    :type reply: string
    :param comment_obj: the comment to reply
    :type comment_obj: praw.models.Comment
    :param pekofy_msg: pekofied message that should only be passed when the reply variable is 'pekofy' to
    pass the pekofied reply to the replies, defaults to None
    :type pekofy_msg: string
    """
    replies["pekofy"]["message"] = pekofy_msg
    if pekofy_msg and is_triggering(pekofy_msg, "nothing changed"):
        reply = "nothing changed"

    reply_content = replies[reply]
    if not random.randint(0, 100) <= (replies[reply]['chance'] if 'chance' in reply_content else 100) or \
            already_replied_to(comment_obj, reply):
        return

    global comments_replied
    comments_replied += 1

    message = random.choice(reply_content["messages"]) if "messages" in replies[reply] else reply_content["message"]
    try:
        comment_obj.reply(message)
    except Exception as e:
        comments_replied -= 1
        print(f"Couldn't reply: {e}")
        notify_author(e, comment_obj, message)
    print(f"{reply}: https://www.reddit.com{comment_obj.permalink}")
    print(f"Reply: {message}")
    print("------------------------")


def already_replied_to(comment, reply):
    """ returns if already replied the same type of comment or not """
    
    second_refresh = False
    for i in range(2):
      try:
          comment.refresh()
          break
      except praw.exceptions.ClientException: # work around as stated in the praw issue 838
          if second_refresh:
              return False
          time.sleep(10)
          second_refresh = True
    comment.replies.replace_more()
    child_comments = comment.replies.list()
    for top_comment in child_comments:
        if top_comment.parent().id != comment.id:
            break
        if top_comment.author == bot_name:
            if "messages" in replies[reply]:
                if top_comment.body in replies[reply]["messages"]:
                    print(f"Already {reply}'d: {top_comment.body} \ncontinuing...")
                    print("------------------------")
                    return True
            else:
                if top_comment.body == replies[reply]["message"]:
                    print(f"Already {reply}'d: {top_comment.body} \ncontinuing...")
                    print("------------------------")
                    return True
    return False


def notify_author(exception, comment=None, tried_reply=None):
    """ Notifies to the author, don't forget to whitelist the bot if your PM's are closed """

    title = datetime.now().strftime("%Y.%m.%d - %H:%M:%S")
    if comment and tried_reply:
        body = f"{bot_name} has run into an error: {exception}\n" \
               f"Here\'s the [link](https://www.reddit.com{comment.permalink}) to the comment.\n" \
               f"Tried to reply this: {tried_reply}"
    else:
        body = f'{bot_name} has run into an error: {exception}\n'
    try:
        reddit.redditor(author).message(title, body)
    except Exception:
        print("Couldn't notify the author")


def is_triggering(text, reply):
    """ whether the text triggers the given reply type or not """

    include_bot = replies[reply]['include_bot'] if 'include_bot' in replies[reply] else False
    if replies[reply]["exact"] if (True if "exact" in replies[reply] else False) else False:
        condition = [True if trigger == text else False for trigger in replies[reply]["triggers"]]
    else:
        condition = [True if trigger in text else False for trigger in replies[reply]["triggers"]]
    if replies[reply]["trigger_type"] == "all":
        return all(condition) and ("bot" in text if include_bot else True)
    return any(condition) and ("bot" in text if include_bot else True)


def passed_limit(comment, limit=2):
    """ returns true if the same comment has been pekofied too much by
    climbing up the comment tree until it reaches the limit """

    current_usage = 0
    for i in range(limit):
        if comment.parent_id == comment.link_id:
            break
        if comment.parent().author == bot_name:
            comment = comment.parent()
            if comment.parent_id == comment.link_id:
                break
            if comment.parent().author and is_triggering(comment.parent().body, "pekofy"):
                comment = comment.parent()
                current_usage += 1
    return current_usage == limit


def is_top_level(comment):
    """ returns if the comment is top level (directly replied to the post) """
    return comment.parent_id == comment.link_id


comments_replied, comments_scanned = 0, 0

# used for exponential back off in case reddit server is unable to respond
initial_wait_time = 10
current_wait_time = initial_wait_time
max_wait_time = 600
reset_limit = 50

while 1:
    try:  # exception handling at it's finest (lol)
        # scan each comment
        for comment in subreddit.stream.comments():
            comments_scanned += 1

            # comment has been deleted or it's author is the bot itself
            if not comment.author or comment.author == bot_name:
                continue

            # pain peko reply
            reply_f("pain peko", comment) if is_triggering(comment.body.lower(), "pain peko") else None

            # hey moona reply
            reply_f("hey moona", comment) if is_triggering(comment.body.lower(), "hey moona") else None

            # feedback gratitude
            replied = False
            if not is_top_level(comment):
                if comment.parent().author:
                    if comment.parent().author.name == bot_name:
                        for feedback in ["thank", "love", "cute", "sorry", "insult"]:
                            if is_triggering(comment.body.lower(), feedback):
                                reply_f(feedback, comment)
                                replied = True
                                break
            if replied:
                continue

            # both pekofy and unpekofy written
            if is_triggering(comment.body, "confused"):
                reply_f("confused", comment)
                continue

            # if keyword found, try to pekofy
            if is_triggering(comment.body, "pekofy"):

                # can't pekofy due to comment not having any parent
                if not comment.parent().author:
                    continue

                # parent is a post, pekofy accordingly
                if is_top_level(comment):
                    reply_f("pekofy", comment, peko.pekofy(
                        comment.submission.title + '\n\n' + comment.submission.selftext if comment.submission.selftext else comment.submission.title))
                    continue

                # someone tried to break it by recursive calling, kindly say no
                if is_triggering(comment.parent().body, "pekofy"):
                    reply_f("no", comment)
                    continue

                # someone tried to pekofy a good/bad bot reply, don't pekofy
                if is_triggering(comment.parent().body.lower(), "bot score abuse"):
                    reply_f("bot score abuse", comment)
                    continue

                # don't pekofy if limit already reached before.
                if comment.parent().body == replies["limit reached"]["message"] and comment.parent().author == bot_name:
                    continue

                # if the same sentence has been pekofied too much already, don't pekofy
                if passed_limit(comment):
                    reply_f("limit reached", comment)
                    continue

                # try to reply to the comment
                reply_f("pekofy", comment, peko.pekofy(comment.parent().body))

            # delete keyphrase found
            if is_triggering(comment.body,
                             "unpekofy") and comment.parent().author == bot_name and comment.parent().body:
                print(f'Unpekofied: {comment.parent().body}')
                comment.parent().delete()
                print("------------------------")

            # More than [reset_limit] comments has been scanned without an incident, reset wait time.
            if comments_scanned % reset_limit == 0:
                current_wait_time = initial_wait_time
    except KeyboardInterrupt:
        print("Keyboard Interrupt. Terminating...")
        break
    except praw.exceptions.RedditAPIException as e:
        print(f"RedditAPIException: {e}")
        notify_author(e)
    except praw.exceptions.PRAWException as e:
        print(f"PRAWException: {e}")
        notify_author(e)
    except Exception as e:
        print(f"Unhandled exception: {e}")
        notify_author(e)
    finally:
        print("------------------------")
        print(f"Replied comments so far: {comments_replied}")
        print(f"Scanned comments so far: {comments_scanned}")
        comments_replied, comments_scanned = 0, 0

        # not-so-exponential back off
        time.sleep(current_wait_time)
        if not current_wait_time > max_wait_time:
            current_wait_time *= 2
