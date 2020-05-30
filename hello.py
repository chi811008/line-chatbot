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

def get_database_connection():
    # Query
    import os
    import psycopg2

    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    return cursor

def get_mountain_name(mountain):
    cursor = get_database_connection()
    postgres_select_query = f"""SELECT * FROM mountain"""

    dic_moun_name = {}
    cursor.execute(postgres_select_query)
    for item in cursor.fetchall():
        dic_moun_name[item[1]] = item

    for name in dic_moun_name.keys():
        if mountain in name:
            return name

def get_mountain(mountain):
    cursor = get_database_connection()

    postgres_select_query = f"""SELECT * FROM mountain"""

    dic_moun = {}
    cursor.execute(postgres_select_query)
    for item in cursor.fetchall():
        dic_moun[item[1]] = item

    for name in dic_moun.keys():
        if mountain in name:
            moun_info = (", ".join(dic_moun[name][1: ]))
    # Query

    return moun_info


def get_mountain_picture(string):
    import requests
    from bs4 import BeautifulSoup
    # string = event.message.text
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
    print("picsoup")
    picture = pic_soup.find("div", {"class": "img-cover cover"}).find("img")["src"]
    return picture


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

@handler.add(PostbackEvent)
def handle_post_message(event):
# can not get event text
    print("event =", event)
    cmd, seq = event.postback.data[:3], event.postback.data[3:]
    if cmd == "inf":
        line_bot_api.reply_message(
                    event.reply_token,
                    TextMessage(
                        text=get_mountain(seq)
                        # text=str(str(event.postback.data)),
                    )
                )
    elif cmd == "pic":
        line_bot_api.reply_message(
                    event.reply_token,
                    ImageSendMessage(
                        original_content_url= seq, preview_image_url= seq)
                        )
    

@handler.add(MessageEvent, message=TextMessage)
def search_info(event):
    search = event.message.text
    if search == "請輸入山的名稱":
        pass
    else:
        picture_url = get_mountain_picture(search)
        button_template_message = ButtonsTemplate(
            thumbnail_image_url=picture_url,
            title = get_mountain_name(search),
            text = '請選擇',
            actions=[
                PostbackTemplateAction(
                    label='山的資訊',
                    text=None,
                    data="inf" + search
                ),
                PostbackTemplateAction(
                    label='大圖',
                    text=None,
                    data="pic" + picture_url
                ),
            ]
        )
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text="Template Example",
                template=button_template_message
            )
        )
            
            
    #      button_template_message =ButtonsTemplate(
    #                              thumbnail_image_url="https://i.imgur.com/eTldj2E.png?1",
    #                              title='Menu',
    #                              text='Please select',
    #                              image_size="cover",
    #                              actions=[
    #  #                                PostbackTemplateAction 點擊選項後，
    #  #                                 除了文字會顯示在聊天室中，
    #  #                                 還回傳data中的資料，可
    #  #                                 此類透過 Postback event 處理。
    #                                  PostbackTemplateAction(
    #                                      label='查詢個人檔案顯示文字-Postback',
    #                                      text='查詢個人檔案',
    #                                      data='action=buy&itemid=1'
    #                                  ),
    #                                  PostbackTemplateAction(
    #                                      label='不顯示文字-Postback',
    #                                      text = None,
    #                                      data='action=buy&itemid=1'
    #                                  ),
    #                                  MessageTemplateAction(
    #                                      label='查詢個人檔案-Message', text='查詢個人檔案'
    #                                  ),
    #                              ]
    #                          )
                             
     
                             
                             
                             
    #      line_bot_api.reply_message(
    #          event.reply_token,
    #          TemplateSendMessage(
    #              alt_text="Template Example",
    #              template=button_template_message
    #          )
    #      )
    
#    line_bot_api.reply_message(
 #       event.reply_token,
  #      TextSendMessage(text=moun_info))


if __name__ == "__main__":
    app.run()

