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
    FlexSendMessage, BubbleContainer, CarouselContainer, ImageComponent, BoxComponent,
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
  select = []
  if ans:
    for _ in ans:
      select.append(_[0])
  else:
      return "很抱歉，沒有符合的資料"
      
  return select




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
  print("event =", event)
  area_list = ["北部", "中部", "南部", "東部", "外島", "香港", "西班牙"]
  receive = event.postback.data
  if get_mountain_name(receive):
    print("get_mountain")
    picture_url = get_mountain_picture(receive)
    bubble = BubbleContainer(
        direction='ltr',
        hero=ImageComponent(
            url=picture_url,
            size='full',
            aspect_ratio='20:13',
            aspect_mode='cover',
            action=PostbackTemplateAction(
                    label='山的圖片',
                    text=None,
                    data="pic" + picture_url
                )
        ),
        body=BoxComponent(
            layout='vertical',
            contents=[
                # title
                TextComponent(text=get_mountain_name(receive), weight='bold', size='xl'),
                # review
                BoxComponent(
                    layout='baseline',
                    margin='md',
                    contents=[
                        TextComponent(text="資訊", size='sm', weight='bold')
                    ]
                ),
                # info
                BoxComponent(
                    layout='vertical',
                    margin='lg',
                    spacing='sm',
                    contents=[
                        BoxComponent(
                            layout='baseline',
                            spacing='sm',
                            contents=[
                                TextComponent(
                                    text='區域',
                                    color='#aaaaaa',
                                    size='sm',
                                    flex=1
                                ),
                                TextComponent(
                                    text=get_mountain(receive)[2],
                                    wrap=True,
                                    color='#666666',
                                    size='sm',
                                    flex=5
                                )
                            ],
                        ),
                        BoxComponent(
                            layout='baseline',
                            spacing='sm',
                            contents=[
                                TextComponent(
                                    text='難度',
                                    color='#aaaaaa',
                                    size='sm',
                                    flex=1
                                ),
                                TextComponent(
                                    text=get_mountain(receive)[3][3:],
                                    wrap=True,
                                    color='#666666',
                                    size='sm',
                                    flex=5,
                                ),
                            ],
                        ),
                        BoxComponent(
                            layout='baseline',
                            spacing='sm',
                            contents=[
                                TextComponent(
                                    text="距離",
                                    color='#aaaaaa',
                                    size='sm',
                                    flex=1
                                ),
                                TextComponent(
                                    text=get_mountain(receive)[4],
                                    wrap=True,
                                    color='#666666',
                                    size='sm',
                                    flex=5,
                                ),
                            ],
                        ),
                        BoxComponent(
                            layout='baseline',
                            spacing='sm',
                            contents=[
                                TextComponent(
                                    text="時間",
                                    color='#aaaaaa',
                                    size='sm',
                                    flex=1
                                ),
                                TextComponent(
                                    text=get_mountain(receive)[5],
                                    wrap=True,
                                    color='#666666',
                                    size='sm',
                                    flex=5,
                                ),
                            ],
                        ),
                    ],
                )
            ],
        ),
        # footer=BoxComponent(
        #     layout='vertical',
        #     spacing='sm',
        #     contents=[
        #         # callAction, separator, websiteAction
        #         SpacerComponent(size='sm'),
        #         # callAction
        #         ButtonComponent(
        #             style='link',
        #             height='sm',
        #             action=URIAction(label='CALL', uri='tel:000000'),
        #         ),
        #         # separator
        #         SeparatorComponent(),
        #         # websiteAction
        #         ButtonComponent(
        #             style='link',
        #             height='sm',
        #             action=URIAction(label='WEBSITE', uri="https://example.com")
        #         )
        #     ]
        # ),
    )
    message = FlexSendMessage(alt_text="山的資訊", contents=bubble)
    line_bot_api.reply_message(
        event.reply_token,
        message
    )
  elif receive in area_list:
    print("cafe cafe cafe")
    select_list = select_area(receive)
    all_bubbles = []
    for _ in select_list:
      bubble1 = f"""{{
        "type": "bubble",
        "size": "micro",
        "hero": {{
          "type": "image",
          "url": "{get_mountain_picture(_)}",
          "size": "full",
          "aspectMode": "cover",
          "aspectRatio": "320:213"
        }},
        "body": {{
          "type": "box",
          "layout": "vertical",
          "contents": [
            {{
              "type": "text",
              "text": "{get_mountain_name(_)}",
              "weight": "bold",
              "size": "sm",
              "wrap": true
            }},
            {{
              "type": "button",
              "action": {{
              "type": "postback",
              "label": "更多資訊",
              "data": "{get_mountain_name(_)}",
              "displayText": "{get_mountain_name(_)}"
              }}
            }}
            ],
            "spacing": "sm",
            "paddingAll": "13px"
          }}
        }}"""
      all_bubbles.append(bubble1)
    print(all_bubbles)

    bubble_string = f"""
    {{
      "type": "carousel",
      "contents": [
        {bubble1},
        {bubble1}
      ]
    }}
    """
    message = FlexSendMessage(
      alt_text="地區篩選", contents=json.loads(bubble_string)
      )
    line_bot_api.reply_message(
      event.reply_token,
      message
      )
  else:
    print("enter_pic")
    cmd, seq = event.postback.data[:3], event.postback.data[3:]
    if cmd == "pic":
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

    elif get_mountain_name(search):
        print("get_mountain")
        picture_url = get_mountain_picture(search)
        
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url=picture_url,
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=PostbackTemplateAction(
                        label='山的圖片',
                        text=None,
                        data="pic" + picture_url
                    )
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text=get_mountain_name(search), weight='bold', size='xl'),
                    # review
                    BoxComponent(
                        layout='baseline',
                        margin='md',
                        contents=[
                            TextComponent(text="資訊", size='sm', weight='bold')
                        ]
                    ),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='區域',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text=get_mountain(search)[2],
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='難度',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text=get_mountain(search)[3][3:],
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text="距離",
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text=get_mountain(search)[4],
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text="時間",
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text=get_mountain(search)[5],
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            # footer=BoxComponent(
            #     layout='vertical',
            #     spacing='sm',
            #     contents=[
            #         # callAction, separator, websiteAction
            #         SpacerComponent(size='sm'),
            #         # callAction
            #         ButtonComponent(
            #             style='link',
            #             height='sm',
            #             action=URIAction(label='CALL', uri='tel:000000'),
            #         ),
            #         # separator
            #         SeparatorComponent(),
            #         # websiteAction
            #         ButtonComponent(
            #             style='link',
            #             height='sm',
            #             action=URIAction(label='WEBSITE', uri="https://example.com")
            #         )
            #     ]
            # ),
        )
       
        message = FlexSendMessage(alt_text="山的資訊", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )


#     elif get_mountain_name(search):
#       print("cafe cafe cafe")
#       bubble1 = f"""{{
#       "type": "bubble",
#       "size": "micro",
#       "hero": {{
#         "type": "image",
#         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip10.jpg",
#         "size": "full",
#         "aspectMode": "cover",
#         "aspectRatio": "320:213"
#       }},
#       "body": {{
#         "type": "box",
#         "layout": "vertical",
#         "contents": [
#           {{
#             "type": "text",
#             "text": "Brown Cafe",
#             "weight": "bold",
#             "size": "sm",
#             "wrap": true
#           }},
#           {{
#             "type": "box",
#             "layout": "baseline",
#             "contents": [
#               {{
#                 "type": "text",
#                 "text": "資訊",
#                 "size": "xs",
#                 "color": "#8c8c8c",
#                 "margin": "md",
#                 "flex": 0
#               }}
#             ]
#           }},
#           {{
#             "type": "box",
#             "layout": "vertical",
#             "contents": [
#               {{
#                 "type": "box",
#                 "layout": "baseline",
#                 "spacing": "sm",
#                 "contents": [
#                   {{
#                     "type": "text",
#                     "text": "東京旅行",
#                     "wrap": true,
#                     "color": "#8c8c8c",
#                     "size": "xs",
#                     "flex": 5
#                   }}
#                 ]
#               }}
#             ]
#           }}
#         ],
#         "spacing": "sm",
#         "paddingAll": "13px"
#       }}
#     }}"""

    
#       bubble_string = f"""
#       {{
#   "type": "carousel",
#   "contents": [
#     {bubble1},
#     {{
#       "type": "bubble",
#       "size": "micro",
#       "hero": {{
#         "type": "image",
#         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip11.jpg",
#         "size": "full",
#         "aspectMode": "cover",
#         "aspectRatio": "320:213"
#       }},
#       "body": {{
#         "type": "box",
#         "layout": "vertical",
#         "contents": [
#           {{
#             "type": "text",
#             "text": "Brow&Cony's Restaurant",
#             "weight": "bold",
#             "size": "sm",
#             "wrap": true
#           }},
#           {{
#             "type": "box",
#             "layout": "baseline",
#             "contents": [
#               {{
#                 "type": "text",
#                 "text": "4.0",
#                 "size": "sm",
#                 "color": "#8c8c8c",
#                 "margin": "md",
#                 "flex": 0
#               }}
#             ]
#           }},
#           {{
#             "type": "box",
#             "layout": "vertical",
#             "contents": [
#               {{
#                 "type": "box",
#                 "layout": "baseline",
#                 "spacing": "sm",
#                 "contents": [
#                   {{
#                     "type": "text",
#                     "text": "東京旅行",
#                     "wrap": true,
#                     "color": "#8c8c8c",
#                     "size": "xs",
#                     "flex": 5
#                   }}
#                 ]
#               }}
#             ]
#           }}
#         ],
#         "spacing": "sm",
#         "paddingAll": "13px"
#       }}
#     }},
#     {{
#       "type": "bubble",
#       "size": "micro",
#       "hero": {{
#         "type": "image",
#         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip12.jpg",
#         "size": "full",
#         "aspectMode": "cover",
#         "aspectRatio": "320:213"
#       }},
#       "body": {{
#         "type": "box",
#         "layout": "vertical",
#         "contents": [
#           {{
#             "type": "text",
#             "text": "Tata",
#             "weight": "bold",
#             "size": "sm"
#           }},
#           {{
#             "type": "box",
#             "layout": "baseline",
#             "contents": [
#               {{
#                 "type": "text",
#                 "text": "4.0",
#                 "size": "sm",
#                 "color": "#8c8c8c",
#                 "margin": "md",
#                 "flex": 0
#               }}
#             ]
#           }},
#           {{
#             "type": "box",
#             "layout": "vertical",
#             "contents": [
#               {{
#                 "type": "box",
#                 "layout": "baseline",
#                 "spacing": "sm",
#                 "contents": [
#                   {{
#                     "type": "text",
#                     "text": "東京旅行",
#                     "wrap": true,
#                     "color": "#8c8c8c",
#                     "size": "xs",
#                     "flex": 5
#                   }}
#                 ]
#               }}
#             ]
#           }}
#         ],
#         "spacing": "sm",
#         "paddingAll": "13px"
#       }}
#     }}
#   ]
# }}
# """
#       message = FlexSendMessage(
#         alt_text="cafe", contents=json.loads(bubble_string)
#         )
#       line_bot_api.reply_message(
#         event.reply_token,
#         message
#         )


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
