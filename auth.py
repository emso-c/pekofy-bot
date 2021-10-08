import praw
import credentials

BOT_NAME = credentials.bot_name
AUTHOR = credentials.author
REDDIT = praw.Reddit(
    client_id=credentials.client_id,
    client_secret=credentials.client_secret,
    username=credentials.bot_name,
    password=credentials.bot_pass,
    user_agent=credentials.user_agent
)