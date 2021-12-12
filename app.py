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
import time
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome('/usr/local/bin/chromedriver',options=options)
driver.get('https://www.nintendo.co.jp/software/campaign/index.html')

soft_name_list = []
while True:
    for element in driver.find_elements_by_class_name("nc3-c-softCard__name"):
        soft_name_list.append(element.text)
    try:
        next_page = driver.find_element_by_class_name("nc3-c-pagination__next")
        next_page.click()
        time.sleep(2)
    except ElementNotInteractableException:
        driver.quit()
        break

app = Flask(__name__)
YOUR_CHANNEL_ACCESS_TOKEN = os.environ['CHANNEL_ACCESS_TOKEN']
YOUR_CHANNEL_SECRET = os.environ['CHANNEL_SECRET']
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

def handle_message(event):
    for list in soft_name_list:
        if event.message.text == list:
            line_bot_api.reply_message(event.reply_token,
        TextSendMessage(text="セール中です")
    )
        else:
            line_bot_api.reply_message(event.reply_token,
        TextSendMessage(text="セール中ではありません")
    )

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
