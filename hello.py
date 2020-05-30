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

def get_mountain(mountain):
    # Query
    import os
    import psycopg2

    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

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
    line_bot_api.reply_message(
                event.reply_token,
                TextMessage(
                    text=get_mountain(event.postback.data)
                    # text=str(str(event.postback.data)),
                )
            )

@handler.add(MessageEvent, message=TextMessage)
def search_info(event):
    search = event.message.text


    if search is not None:
        button_template_message = ButtonsTemplate(
            thumbnail_image_url="https://i.imgur.com/eTldj2E.png?1",
            title=search,
            text='請選擇',
            actions=[
                PostbackTemplateAction(
                    label='山的資訊',
                    text=None,
                    data=search
                )
            ]
        )

        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text="Template Example",
                template=button_template_message
            )
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='hello'))
            
            
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

