from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    ImageSendMessage, MessageEvent, PostbackEvent,
    TextSendMessage, TemplateSendMessage,
    TextMessage, ButtonsTemplate,
    PostbackTemplateAction, MessageTemplateAction,
    URITemplateAction, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('K9VIeDOz0f7pg/kQMrqggOjd5rOcLwMYOg2PlrBJuQDpX3p1Q/o4+cuK6VapoA5q+j0QLdxZwwLu8as9S3Hi4gblljWUIEWAFG7i/4YzoEPBovw6yb6h2bZrLdeyB++yb4WTtzqSOJmPSPszvo2KwAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e365002afec95950d148063ee819297f')

@app.route('/')
def hello_world():
    return 'Hello, World! My name is Seraphine. I am happy now'

@app.route('/test')
def test_page():
    return 'In test page!'



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
    if event.message.text == "文字":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
    elif event.message.text == "Yes":
        line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=11539, sticker_id=52114123))
    elif event.message.text == "OK":
        line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=11539, sticker_id=52114113))
    elif event.message.text == "圖片":
        pic = "https://s.yimg.com/ny/api/res/1.2/12UU2JphAsbxTTDca.7QFQ--~A/YXBwaWQ9aGlnaGxhbmRlcjtzbT0xO3c9MTA4MDtoPTcxNg--/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/7b5b5330-112b-11ea-a77f-7c019be7ecae"
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url= pic, preview_image_url= pic))
    elif event.message.text == "請輸入山的名稱":
        import requests
        from bs4 import BeautifulSoup
        string = event.message.text
        url = "https://hiking.biji.co/index.php?q=trail&part=全部&city=全部&zip=全部&time=全部&level=全部&type=全部&keyword="
        search = url + string
        re = requests.get(search)
        soup = BeautifulSoup(re.text, "html.parser")
        data = soup.find("div", {"class": "postMeta-feedSummery"}).find("a")["href"]
        web = "https://hiking.biji.co" + data
        print(web)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=web))
        
        
        
        
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))





if __name__ == "__main__":
    app.run()
