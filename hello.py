import json

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, PostbackEvent,
    TextSendMessage, TemplateSendMessage,
    TextMessage, ButtonsTemplate,
    PostbackTemplateAction, MessageTemplateAction,
    URITemplateAction, StickerSendMessage,
    CarouselTemplate, CarouselColumn,
)

app = Flask(__name__)


line_bot_api = LineBotApi('K9VIeDOz0f7pg/kQMrqggOjd5rOcLwMYOg2PlrBJuQDpX3p1Q/o4+cuK6VapoA5q+j0QLdxZwwLu8as9S3Hi4gblljWUIEWAFG7i/4YzoEPBovw6yb6h2bZrLdeyB++yb4WTtzqSOJmPSPszvo2KwAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e365002afec95950d148063ee819297f')


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
def picture(event):
    try:
        import requests
        from bs4 import BeautifulSoup
        string = event.message.text
        url = "https://hiking.biji.co/index.php?q=trail&part=全部&city=全部&zip=全部&time=全部&level=全部&type=全部&keyword="
        search = url + string
        re = requests.get(search)
        soup = BeautifulSoup(re.text, "html.parser")
        data = soup.find("div", {"class": "postMeta-feedSummery"}).find("a")["href"]
        web = "https://hiking.biji.co" + data
        re_pic = requests.get(web)
        pic_soup = BeautifulSoup(re_pic.text, "html.parser")
        #picture = pic_soup.find("div", {"class": "img-cover cover"}).find("img")["src"]
        picture = "https://cdntwrunning.biji.co/800_7885322f41fd94d458c5a5c9f4b4ba1b59ba5bc13777a4c144a25c7da3dd7dfd.jpg"
        pic = "https://s.yimg.com/ny/api/res/1.2/12UU2JphAsbxTTDca.7QFQ--~A/YXBwaWQ9aGlnaGxhbmRlcjtzbT0xO3c9MTA4MDtoPTcxNg--/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/7b5b5330-112b-11ea-a77f-7c019be7ecae"
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url= pic, preview_image_url= pic))
    except:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = event.message.text)
        )
        pass


if __name__ == "__main__":
    app.run()
