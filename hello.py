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
def picture(event):
    print("mack sure the func activate")
    try:
        import requests
        from bs4 import BeautifulSoup
        string = event.message.text
        print("mack sure the func activate into try")
        url = "https://hiking.biji.co/index.php?q=trail&part=全部&city=全部&zip=全部&time=全部&level=全部&type=全部&keyword="
        search = url + string
        print("search")
        re = requests.get(search)
        print("re")
        soup = BeautifulSoup(re.text, "html.parser")
        print("soup")
        data = soup.find("div", {"class": "postMeta-feedSummery"}).find("a")["href"]
        print("data")
        web = "https://hiking.biji.co" + data
        re_pic = requests.get(web)
        print("repic")
        pic_soup = BeautifulSoup(re_pic.text, "html.parser")
        picture = pic_soup.find("div", {"class": "img-cover cover"}).find("img")["src"]
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url= picture, preview_image_url= picture))
    except:
        print("mack sure the func activite into except")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = event.message.text)
        )
        pass






if __name__ == "__main__":
    app.run()

