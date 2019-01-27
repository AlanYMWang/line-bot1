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

line_bot_api = LineBotApi('2zhhhrmlgtwrrDSOtbh8fZadIRf+qRlK0/+gUnBNVPY9os1JpTLl+F3OCUYUscmKTlIiCGSB61lcGliGPjTJ0wwtcgq98c9nTAIXhomBil8Pa4OSIERiytai+A4ac9CYh8k+2ubcmVgDJAt3Z9VNdgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('97e77d6ad510fe99e515a21a46005f4e')


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