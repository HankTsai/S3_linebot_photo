

from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)


import boto3
s3_client = boto3.client(
    's3',
    aws_access_key_id='AKIAR4NDUH53GWDLQFNM',
    aws_secret_access_key='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')

app = Flask(__name__)
line_bot_api = LineBotApi('QsvdgY7ICz6byG2pQtuE9WqqJ9lbTlC6tCZQk6Gvt0WMUikZFk8EcuZWoaQlMizaLvTP8GeWrwRrDSa9pEaj7Ev0uzyzW6chMynSaiM3lZb5t/uWeDGx1g1jERL93njJ40hKUTNfVnstuPPJtBJDxQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('fa8f660ff3d18c6db4e4ce24da6e3d87')

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

from linebot.models import ImageMessage
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    # 把圖片用id當作檔名，存回本地端
    file_path = event.message.id + '.jpg'
    with open(file_path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
    # s3_client 上傳圖片到bucket
    s3_client.upload_file(file_path, "iii-tutorial-v2", "student24/" + file_path)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage("哈哈哈收到囉!。"))

if __name__ == "__main__":
    app.run()
