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

import os
app = Flask(__name__)
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["cjPUXRyUefw9WY+cagR5i8KGdaFWZ+A9ExlDnRJwvDpL40Cv7x+4gl5YP2/oEygo3nTEO5FMk37OS1Er0JOwjDBK/ugCYCEqa5nlGBgz+mMhJnCnzDYl3MR7e4EBfd3oceKLWu/9Fvin4gF6djgpMgdB04t89/1O/w1cDnyilFU="]
YOUR_CHANNEL_SECRET = os.environ["b73dd305b4792462085ecc766936b235"]
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
#オウム返し用のメッセージイベント
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
