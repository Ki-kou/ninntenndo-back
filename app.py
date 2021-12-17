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
import psycopg2
import os

app = Flask(__name__)
YOUR_CHANNEL_ACCESS_TOKEN = os.environ['CHANNEL_ACCESS_TOKEN']
YOUR_CHANNEL_SECRET = os.environ['CHANNEL_SECRET']
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
conn.set_client_encoding('utf-8') 
cursor = conn.cursor()
cursor.execute('SELECT title FROM data ')
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

results = cursor.fetchall()

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
    if event.message.text in results:
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="セール中です")
    )
    else:
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="セール中ではありません")
    )
    
if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
