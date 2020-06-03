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
    URITemplateAction, StickerSendMessage, FlexSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi(
    'K9VIeDOz0f7pg/kQMrqggOjd5rOcLwMYOg2PlrBJuQDpX3p1Q/o4+cuK6VapoA5q+j0QLdxZwwLu8as9S3Hi4gblljWUIEWAFG7i/4YzoEPBovw6yb6h2bZrLdeyB++yb4WTtzqSOJmPSPszvo2KwAdB04t89/1O/w1cDnyilFU=')
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

    postgres_select_query = f"""SELECT mountain_name FROM mountain WHERE mountain_name LIKE '%{mountain}%' LIMIT 1"""
    cursor.execute(postgres_select_query)
    data_exist = cursor.fetchall()
    if data_exist:
        return data_exist[0][0]
    else:
        return False


def get_mountain(mountain):
    cursor = get_database_connection()

    postgres_select_query = f"""SELECT * FROM mountain WHERE mountain_name LIKE '%{mountain}%' LIMIT 1"""
    cursor.execute(postgres_select_query)

    for _ in cursor.fetchall():
        moun_info = ", ".join(_[1:])
    # Query

    return moun_info


def get_mountain_picture(string):
    import requests
    from bs4 import BeautifulSoup
    url = "https://hiking.biji.co/index.php?q=trail&part=全部&city=全部&zip=全部&time=全部&level=全部&type=全部&keyword="
    search = url + string
    re = requests.get(search)
    soup = BeautifulSoup(re.text, "html.parser")
    data = soup.find(
        "div", {"class": "postMeta-feedSummery"}).find("a")["href"]
    web = "https://hiking.biji.co" + data
    re_pic = requests.get(web)
    pic_soup = BeautifulSoup(re_pic.text, "html.parser")
    picture = pic_soup.find(
        "div", {"class": "img-cover cover"}).find("img")["src"]
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
                original_content_url=seq, preview_image_url=seq)
        )


index = {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://ithelp.ithome.com.tw/images/ironman/11th/event/kv_event/kv-bg-addfly.png",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
          "type": "uri",
          "uri": "http://linecorp.com/"
        },
        "backgroundColor": "#FFFFFF"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "區域",
            "weight": "bold",
            "size": "xl",
            "margin": "md"
          }
        ],
        "action": {
          "type": "uri",
          "label": "action",
          "uri": "http://linecorp.com/"
        }
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "北部",
              "data": "北部"
            },
            "height": "sm"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "中部",
              "data": "中部"
            },
            "height": "sm"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "南部",
              "data": "南部"
            },
            "height": "sm"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "東部",
              "data": "東部"
            },
            "height": "sm"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "外島",
              "data": "外島"
            },
            "height": "sm"
          }
        ],
        "flex": 0
      },
      "styles": {
        "footer": {
          "separator": True
        }
      }
    },
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://ithelp.ithome.com.tw/images/ironman/11th/event/kv_event/kv-bg-addfly.png",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
          "type": "uri",
          "uri": "http://linecorp.com/"
        },
        "backgroundColor": "#FFFFFF"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "難度",
            "weight": "bold",
            "size": "xl",
            "margin": "md"
          }
        ],
        "action": {
          "type": "uri",
          "label": "View detail",
          "uri": "http://linecorp.com/",
          "altUri": {
            "desktop": "http://example.com/page/123"
          }
        }
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "低",
              "data": "低"
            },
            "height": "sm"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "低-中",
              "data": "低-中"
            },
            "height": "sm"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "中",
              "data": "中"
            },
            "height": "sm"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "中-高",
              "data": "中-高"
            },
            "height": "md"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "高",
              "data": "高"
            },
            "height": "md"
          }
        ],
        "flex": 0
      },
      "styles": {
        "footer": {
          "separator": True
        }
      }
    },
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://ithelp.ithome.com.tw/images/ironman/11th/event/kv_event/kv-bg-addfly.png",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
          "type": "uri",
          "uri": "http://linecorp.com/"
        },
        "backgroundColor": "#FFFFFF"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "時間",
            "weight": "bold",
            "size": "xl",
            "margin": "md"
          }
        ],
        "action": {
          "type": "uri",
          "label": "View detail",
          "uri": "http://linecorp.com/",
          "altUri": {
            "desktop": "http://example.com/page/123"
          }
        }
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "3小時內",
              "data": "3小時內"
            },
            "height": "sm"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "3-6小時",
              "data": "3-6小時"
            },
            "height": "sm"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "6小時-12小時",
              "data": "6小時-12小時"
            },
            "height": "sm"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "12小時-兩天",
              "data": "12小時-兩天"
            },
            "height": "sm"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "兩天以上",
              "data": "兩天以上"
            },
            "height": "sm"
          }
        ],
        "flex": 0
      },
      "styles": {
        "footer": {
          "separator": True
        }
      }
    }
  ]
}


@handler.add(MessageEvent, message=TextMessage)
def search_info(event):
    search = event.message.text
    if search == "請輸入山的名稱":
        print("搜尋")
        pass

    elif search == "篩選":
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="篩選",
                contents=index
            )
        )
    elif get_mountain_name(search):
        print("get_mountain")
        picture_url = get_mountain_picture(search)
        button_template_message = ButtonsTemplate(
            thumbnail_image_url=picture_url,
            title=get_mountain_name(search),
            text='請選擇',
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
    else:
        print("exceptions")
        text = "抱歉，您搜尋的資料不存在，請重新輸入"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=text
            )
        )


if __name__ == "__main__":
    app.run()
