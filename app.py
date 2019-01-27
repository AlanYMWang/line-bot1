from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('UScYbuKk2VLtsHmewpBljvdU4kB1cmCA+Wq2e1sxooV3kMiq4znP+/h70ORnR+yKnqzYz2MCYE7naPpsKvqY7jkMUXBBMmiWnzJzDctGG94q45xke98BdL/5LHBNmdzYJGHuDXM3nODjY19K5x7h5gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b25f16b09da4d0b660663a584d9eded6')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text

    if msg in ["組長好", "你好" ,"您好"]:
        re = "我是新上任的核儀組組長，大家好!!"
    elif msg in ["張永瑞","張東西","髒"]:
        re = "我正在出國爽，等我回國再說"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=re))


if __name__ == "__main__":
    app.run()