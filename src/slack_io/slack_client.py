import time
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt import App
from slack_sdk.errors import SlackApiError
import os, logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

log = logging.getLogger(__name__)

app = App(token=os.getenv("SLACK_BOT_TOKEN"))

def post_message(channel: str, text: str, username: str, icon_emoji: str=None, thread_ts: str=None):
    args = {
        "channel": channel,
        "text": text,
        "username": username,   
    }

    if icon_emoji:
        args["icon_emoji"] = icon_emoji
    if thread_ts:
        args["threads_ts"] = thread_ts
    while True:
        try:
            return app.client.chat_postMessage(**args)
        except SlackApiError as e:
            if e.response.status_code == 429:
                wait = int(e.response.headers.get("Retry-After", "1"))
                time.sleep(wait + 0.1)
                continue
            raise

def fetch_history(channel: str, oldest: str=None, latest: str=None, limit: int=200):
    return app.client.conversations.history(channel=channel, oldest=oldest, latest=latest, limit=limit)

def fetch_thread(channel: str, parent_ts: str, limit: int=200):
    return app.client.conversations.replies(channel=channel, ts=parent_ts, limit=limit)
    