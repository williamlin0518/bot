import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from myMessage import *
from fsm import TocMachine
from utils import send_text_message

rand = 0
load_dotenv()

machine = TocMachine(
    states=["user", "menu", "whichKind", "random", "all", "crime", "romance", "adventure", "action", "fantasy",
            "biography", "intro", "fsm", 'randomDetail'],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "random",
            "conditions": "is_going_to_random",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "whichKind",
            "conditions": "is_going_to_whichKind",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "fsm",
            "conditions": "is_going_to_fsm",
        },
        {
            "trigger": "advance",
            "source": "random",
            "dest": "random",
            "conditions": "is_going_to_random",
        },
        {
            "trigger": "advance",
            "source": "whichKind",
            "dest": "all",
            "conditions": "is_going_to_all",
        },
        {
            "trigger": "advance",
            "source": "whichKind",
            "dest": "crime",
            "conditions": "is_going_to_crime",
        },
        {
            "trigger": "advance",
            "source": "whichKind",
            "dest": "romance",
            "conditions": "is_going_to_romance",
        },
        {
            "trigger": "advance",
            "source": "whichKind",
            "dest": "adventure",
            "conditions": "is_going_to_adventure",
        },
        {
            "trigger": "advance",
            "source": "whichKind",
            "dest": "action",
            "conditions": "is_going_to_action",
        },
        {
            "trigger": "advance",
            "source": "whichKind",
            "dest": "fantasy",
            "conditions": "is_going_to_fantasy",
        },
        {
            "trigger": "advance",
            "source": "whichKind",
            "dest": "biography",
            "conditions": "is_going_to_biography",
        },
        {
            "trigger": "advance",
            "source": "random",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "random",
            "dest": "randomDetail",
            "conditions": "is_going_to_randomDetail",
        },
        {
            "trigger": "advance",
            "source": "all",
            "dest": "intro",
            "conditions": "is_going_to_intro",
        },
        {
            "trigger": "advance",
            "source": "crime",
            "dest": "intro",
            "conditions": "is_going_to_intro",
        },
        {
            "trigger": "advance",
            "source": "romance",
            "dest": "intro",
            "conditions": "is_going_to_intro",
        },
        {
            "trigger": "advance",
            "source": "adventure",
            "dest": "intro",
            "conditions": "is_going_to_intro",
        },
        {
            "trigger": "advance",
            "source": "action",
            "dest": "intro",
            "conditions": "is_going_to_intro",
        },
        {
            "trigger": "advance",
            "source": "fantasy",
            "dest": "intro",
            "conditions": "is_going_to_intro",
        },
        {
            "trigger": "advance",
            "source": "biography",
            "dest": "intro",
            "conditions": "is_going_to_intro",
        },
        {
            "trigger": "advance",
            "source": "crime",
            "dest": "whichKind",
            "conditions": "is_going_to_intro",
        },

        {"trigger": "go_back",
         "source": ["menu", "whichKind", "random", "all", "crime", "romance", "adventure", "action", "fantasy",
                    "biography", "intro", "fsm", "randomDetail"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue

        response = machine.advance(event)
        # send_text_message(event.reply_token, "不懂你要幹嘛")

        if not response:
            if machine.state == 'crime':
                send_text_message(event.reply_token, '請認真輸入')
            elif machine.states == 'all':
                send_text_message(event.reply_token, '請認真輸入')
            else:
                send_text_message(event.reply_token, "不懂你要幹嘛")

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


# def massage_handler(input, line_bot_api,event):
#     if '最新合作廠商' in input:
#         message = imagemap_message()
#         line_bot_api.reply_message(event.reply_token, message)
#

if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
    show_fsm()
