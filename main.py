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

#環境変数取得
# LINE Developersで設定されているアクセストークンとChannel Secretをを取得し、設定します。
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["cjPUXRyUefw9WY+cagR5i8KGdaFWZ+A9ExlDnRJwvDpL40Cv7x+4gl5YP2/oEygo3nTEO5FMk37OS1Er0JOwjDBK/ugCYCEqa5nlGBgz+mMhJnCnzDYl3MR7e4EBfd3oceKLWu/9Fvin4gF6djgpMgdB04t89/1O/w1cDnyilFU="]
YOUR_CHANNEL_SECRET = os.environ["b73dd305b4792462085ecc766936b235"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


## 1 ##
#Webhookからのリクエストをチェックします。
@app.route("/callback", methods=['POST'])
def callback():
    # リクエストヘッダーから署名検証のための値を取得します。
    signature = request.headers['X-Line-Signature']

    # リクエストボディを取得します。
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
        TextSendMessage(text=event.message.text))  # ここでオウム返しのメッセージを返します。


# ポート番号の設定
if __name__ == "__main__":
    #    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
