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

line_bot_api = LineBotApi('/8Rjr1iQja+JEcKZdKkVY91zHP4vTpBFt9C4rEDHc0h1uI2m3avoN8F92vBa5uURTlIiCGSB61lcGliGPjTJ0wwtcgq98c9nTAIXhomBil9wwGt4mJVlDLLZRSFW4k7eGyFQnKTEkfZKVohkiYfRdwdB04t89/1O/w1cDnyilFU=
')
handler = WebhookHandler('68abaeb22e280a2219174b9fcfe530f1')


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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()