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

  postgres_select_query = f"""SELECT mountain_name FROM mountain WHERE area = '{input_area}' LIMIT 10 """

  cursor.execute(postgres_select_query)
  ans = cursor.fetchall()
  select = []
  if ans:
    for _ in ans:
      select.append(_[0])
    return select
  else:
      return "很抱歉，沒有符合的資料"
      

def select_difficulty(input_difficulty):
  cursor = get_database_connection()

  postgres_select_query = f"""SELECT mountain_name FROM mountain WHERE difficulty_int = '{input_difficulty}' LIMIT 10 """

  cursor.execute(postgres_select_query)
  ans = cursor.fetchall()
  select = []
  if ans:
    for _ in ans:
      select.append(_[0])
    return select
  else:
      return "很抱歉，沒有符合的資料"
      

def select_time(input_time):
  cursor = get_database_connection()

  if input_time == "0":
    postgres_select_query = f"""SELECT mountain_name FROM mountain WHERE time_int < 180 LIMIT 10 """
  elif input_time == "1":
    postgres_select_query = f"""SELECT mountain_name FROM mountain WHERE time_int < 360 and time_int >= 180 LIMIT 10 """
  elif input_time == "2":
    postgres_select_query = f"""SELECT mountain_name FROM mountain WHERE time_int < 720 and time_int >= 360 LIMIT 10 """
  elif input_time == "3":
    postgres_select_query = f"""SELECT mountain_name FROM mountain WHERE time_int < 2880 and time_int >= 720 LIMIT 10 """
  elif input_time == "4":
    postgres_select_query = f"""SELECT mountain_name FROM mountain WHERE time_int >= 2880 LIMIT 10 """

  cursor.execute(postgres_select_query)
  ans = cursor.fetchall()
  select = []
  if ans:
    for _ in ans:
      select.append(_[0])
    return select
  else:
      return "很抱歉，沒有符合的資料"
      



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
  else:
    cmd, seq = receive[:3], receive[3:]
    if cmd == "are":
      print("area_north_east_west_south")
      select_list = select_area(seq)
    elif cmd == "dif":
      select_list = select_difficulty(seq)
    elif cmd == "tim":
      select_list = select_time(seq)

    if select_list == "很抱歉，沒有符合的資料":
      print("no_information")
      line_bot_api.reply_message(
          event.reply_token,
          TextSendMessage(
              text=select_list
          )
      )
    else:
      print("select_list_has_mountain")
      all_bubbles = []
      for _ in select_list:
        bubble = {
          "type": "bubble",
          "size": "micro",
          "hero": {
            "type": "image",
            "url": "url",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "320:213"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "Brown Cafe",
                "weight": "bold",
                "size": "lg",
                "wrap": True,
              },
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "更多資訊",
                  "data": "var",
                  "displayText": "var"
                }
              }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
          }
        }
        bubble["hero"]["url"] = get_mountain_picture(_)
        get_name = get_mountain_name(_)
        bubble["body"]["contents"][0]["text"] = get_name
        bubble["body"]["contents"][1]["action"]["data"] = get_name
        bubble["body"]["contents"][1]["action"]["displayText"] = get_name
        all_bubbles.append(bubble)
        print(get_name)
      bubble_string = {
        "type": "carousel",
          "contents": all_bubbles
      }
      message = FlexSendMessage(
        alt_text="篩選", contents=bubble_string
        )
      line_bot_api.reply_message(
        event.reply_token,
        message
        )

@handler.add(MessageEvent, message=TextMessage)
def search_info(event):
    search = event.message.text
    if search == "請輸入山的名稱":
      print("搜尋")
      pass

    elif search == "篩選":
      bubble_string = {
        "type": "carousel",
        "contents": [
          {
            "type": "bubble",
            "hero": {
              "type": "image",
              "url": "url",
              "size": "full",
              "aspectRatio": "20:13",
              "aspectMode": "cover",
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
              ]
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
                    "data": "are北部"
                  },
                  "height": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "postback",
                    "label": "中部",
                    "data": "are中部"
                  },
                  "height": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "postback",
                    "label": "南部",
                    "data": "are南部"
                  },
                  "height": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "postback",
                    "label": "東部",
                    "data": "are東部"
                  },
                  "height": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "postback",
                    "label": "外島",
                    "data": "are外島"
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
              "url": "url",
              "size": "full",
              "aspectRatio": "20:13",
              "aspectMode": "cover",
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
              ]
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
                    "data": "dif0"
                  },
                  "height": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "postback",
                    "label": "低-中",
                    "data": "dif1"
                  },
                  "height": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "postback",
                    "label": "中",
                    "data": "dif2"
                  },
                  "height": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "postback",
                    "label": "中-高",
                    "data": "dif3"
                  },
                  "height": "md"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "postback",
                    "label": "高",
                    "data": "dif4"
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
              "url": "url",
              "size": "full",
              "aspectRatio": "20:13",
              "aspectMode": "cover",
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
              ]
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
                    "data": "tim0"
                  },
                  "height": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "postback",
                    "label": "3-6小時",
                    "data": "tim1"
                  },
                  "height": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "postback",
                    "label": "6小時-12小時",
                    "data": "tim2"
                  },
                  "height": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "postback",
                    "label": "12小時-兩天",
                    "data": "tim3"
                  },
                  "height": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "postback",
                    "label": "兩天以上",
                    "data": "tim4"
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
      area_pic_url = ""
      difficulity_pic_url = ""
      time_pic_url = "https://imagizer.imageshack.com/img923/7386/5tG2SO.jpg"
      bubble_string["contents"][0]["hero"]["url"] = area_pic_url
      bubble_string["contents"][1]["hero"]["url"] = difficulity_pic_url
      bubble_string["contents"][2]["hero"]["url"] = time_pic_url

      message = FlexSendMessage(
          alt_text="篩選", contents=bubble_string
          )
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
