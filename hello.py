from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage, PostbackTemplateAction, MessageTemplateAction,
    URITemplateAction)

import json

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

    return cursor.fetchall()[0]


def get_mountain_picture(mountain):
    cursor = get_database_connection()

    postgres_select_query = f"""SELECT pic FROM mountain WHERE mountain_name LIKE '%{mountain}%' LIMIT 1"""
    cursor.execute(postgres_select_query)

    return cursor.fetchall()[0][0]

def select_area(input_area):
  cursor = get_database_connection()

  postgres_select_query = f"""SELECT mountain_name FROM mountain WHERE area = '{input_area}' LIMIT 5 """

  cursor.execute(postgres_select_query)
  ans = cursor.fetchall()
  if ans:
      string = ""
      for _ in ans:
          string = string + _[0] + ","
  else:
      return "很抱歉，沒有符合的資料"
      
  return string




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
    if event.postback.data == "北部" or "中部" or "南部" or "東部" or "外島" or "香港" or "西班牙":
      replytex = select_area(event.postback.data)
      line_bot_api.reply_message(
            event.reply_token,
            TextMessage(
                text=replytex
                # text=str(str(event.postback.data)),
            )
        )
    else:
      cmd, seq = event.postback.data[:3], event.postback.data[3:]
      if cmd == "inf":
          print("informaton show")
          line_bot_api.reply_message(
              event.reply_token,
              TextMessage(
                  text=get_mountain(seq)
                  # text=str(str(event.postback.data)),
              )
          )
      elif cmd == "pic":
          print("picture show")
          line_bot_api.reply_message(
              event.reply_token,
              ImageSendMessage(
                  original_content_url=seq, preview_image_url=seq)
          )


@handler.add(MessageEvent, message=TextMessage)
def search_info(event):
    search = event.message.text
    if search == "請輸入山的名稱":
        print("搜尋")
        pass

    elif search == "篩選":
        bubble_string = """
        {
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
          "separator": true
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
          "separator": true
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
          "separator": true
        }
      }
    }
  ]
}
        """
        message = FlexSendMessage(
            alt_text="篩選", contents=json.loads(bubble_string))
        line_bot_api.reply_message(
            event.reply_token,
            message
        )

    # elif get_mountain_name(search):
    #     print("get_mountain")
    #     picture_url = get_mountain_picture(search)
        
    #     bubble = BubbleContainer(
    #         direction='ltr',
    #         hero=ImageComponent(
    #             url=picture_url,
    #             size='full',
    #             aspect_ratio='20:13',
    #             aspect_mode='cover',
    #             action=PostbackTemplateAction(
    #                     label='山的圖片',
    #                     text=None,
    #                     data="pic" + picture_url
    #                 )
    #         ),
    #         body=BoxComponent(
    #             layout='vertical',
    #             contents=[
    #                 # title
    #                 TextComponent(text=get_mountain_name(search), weight='bold', size='xl'),
    #                 # review
    #                 BoxComponent(
    #                     layout='baseline',
    #                     margin='md',
    #                     contents=[
    #                         TextComponent(text="資訊", size='sm', weight='bold')
    #                     ]
    #                 ),
    #                 # info
    #                 BoxComponent(
    #                     layout='vertical',
    #                     margin='lg',
    #                     spacing='sm',
    #                     contents=[
    #                         BoxComponent(
    #                             layout='baseline',
    #                             spacing='sm',
    #                             contents=[
    #                                 TextComponent(
    #                                     text='區域',
    #                                     color='#aaaaaa',
    #                                     size='sm',
    #                                     flex=1
    #                                 ),
    #                                 TextComponent(
    #                                     text=get_mountain(search)[2],
    #                                     wrap=True,
    #                                     color='#666666',
    #                                     size='sm',
    #                                     flex=5
    #                                 )
    #                             ],
    #                         ),
    #                         BoxComponent(
    #                             layout='baseline',
    #                             spacing='sm',
    #                             contents=[
    #                                 TextComponent(
    #                                     text='難度',
    #                                     color='#aaaaaa',
    #                                     size='sm',
    #                                     flex=1
    #                                 ),
    #                                 TextComponent(
    #                                     text=get_mountain(search)[3][3:],
    #                                     wrap=True,
    #                                     color='#666666',
    #                                     size='sm',
    #                                     flex=5,
    #                                 ),
    #                             ],
    #                         ),
    #                         BoxComponent(
    #                             layout='baseline',
    #                             spacing='sm',
    #                             contents=[
    #                                 TextComponent(
    #                                     text="距離",
    #                                     color='#aaaaaa',
    #                                     size='sm',
    #                                     flex=1
    #                                 ),
    #                                 TextComponent(
    #                                     text=get_mountain(search)[4],
    #                                     wrap=True,
    #                                     color='#666666',
    #                                     size='sm',
    #                                     flex=5,
    #                                 ),
    #                             ],
    #                         ),
    #                         BoxComponent(
    #                             layout='baseline',
    #                             spacing='sm',
    #                             contents=[
    #                                 TextComponent(
    #                                     text="時間",
    #                                     color='#aaaaaa',
    #                                     size='sm',
    #                                     flex=1
    #                                 ),
    #                                 TextComponent(
    #                                     text=get_mountain(search)[5],
    #                                     wrap=True,
    #                                     color='#666666',
    #                                     size='sm',
    #                                     flex=5,
    #                                 ),
    #                             ],
    #                         ),
    #                     ],
    #                 )
    #             ],
    #         ),
    #         # footer=BoxComponent(
    #         #     layout='vertical',
    #         #     spacing='sm',
    #         #     contents=[
    #         #         # callAction, separator, websiteAction
    #         #         SpacerComponent(size='sm'),
    #         #         # callAction
    #         #         ButtonComponent(
    #         #             style='link',
    #         #             height='sm',
    #         #             action=URIAction(label='CALL', uri='tel:000000'),
    #         #         ),
    #         #         # separator
    #         #         SeparatorComponent(),
    #         #         # websiteAction
    #         #         ButtonComponent(
    #         #             style='link',
    #         #             height='sm',
    #         #             action=URIAction(label='WEBSITE', uri="https://example.com")
    #         #         )
    #         #     ]
    #         # ),
    #     )
    #     message = FlexSendMessage(alt_text="山的資訊", contents=bubble)
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         message
    #     )


    #     # button_template_message = ButtonsTemplate(
    #     #     thumbnail_image_url=picture_url,
    #     #     title=get_mountain_name(search),
    #     #     text='請選擇',
    #     #     actions=[
    #     #         PostbackTemplateAction(
    #     #             label='山的資訊',
    #     #             text=None,
    #     #             data="inf" + search
    #     #         ),
    #     #         PostbackTemplateAction(
    #     #             label='大圖',
    #     #             text=None,
    #     #             data="pic" + picture_url
    #     #         ),
    #     #     ]
    #     # )
    #     # line_bot_api.reply_message(
    #     #     event.reply_token,
    #     #     TemplateSendMessage(
    #     #         alt_text="Template Example",
    #     #         template=button_template_message
    #     #     )
    #     # )
    elif get_mountain_name(search):
      print("cafe cafe cafe")
      bubble_string = f"""
      {{
  "type": "bubble",
  "hero": {{
    "type": "image",
    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {{
      "type": "uri",
      "uri": "http://linecorp.com/"
    }}
  }},
  "body": {{
    "type": "box",
    "layout": "vertical",
    "contents": [
      {{
        "type": "text",
        "text": {get_mountain_name(search)},
        "weight": "bold",
        "size": "xl"
      }},
      {{
        "type": "box",
        "layout": "baseline",
        "margin": "md",
        "contents": [
          {{
            "type": "text",
            "text": "資訊",
            "size": "sm",
            "color": "#999999",
            "margin": "md",
            "flex": 0,
            "weight": "bold"
          }}
        ]
      }},
      {{
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {{
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {{
                "type": "text",
                "text": "Place",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              }},
              {{
                "type": "text",
                "text": "Miraina Tower, 4-1-6 Shinjuku, Tokyo",
                "wrap": true,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }}
            ]
          }},
          {{
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {{
                "type": "text",
                "text": "Time",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              }},
              {{
                "type": "text",
                "text": "10:00 - 23:00",
                "wrap": true,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }}
            ]
          }}
        ]
      }}
    ]
  }}
}}
"""
      message = FlexSendMessage(
        alt_text="篩選", contents=json.loads(bubble_string)
        )
      line_bot_api.reply_message(
        event.reply_token,
        message
        )


    elif search == '圖片輪播':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerAction(label='datetime',
                                                            data='datetime_postback',
                                                            mode='datetime')),
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerAction(label='date',
                                                            data='date_postback',
                                                            mode='date'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    
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
