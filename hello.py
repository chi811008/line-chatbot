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

def select_area(input_area, page = 0):
  cursor = get_database_connection()

  postgres_select_query = f"""SELECT mountain_name FROM mountain WHERE area = '{input_area}' LIMIT 9 OFFSET {page}"""

  cursor.execute(postgres_select_query)
  ans = cursor.fetchall()
  select = []
  if ans:
    for _ in ans:
      select.append(_[0])
    return select
  else:
      return "很抱歉，沒有符合的資料"
      

def select_difficulty(input_difficulty, page = 0):
  cursor = get_database_connection()

  postgres_select_query = f"""SELECT mountain_name FROM mountain WHERE difficulty_int = '{input_difficulty}' LIMIT 9 OFFSET {page}"""

  cursor.execute(postgres_select_query)
  ans = cursor.fetchall()
  select = []
  if ans:
    for _ in ans:
      select.append(_[0])
    return select
  else:
      return "很抱歉，沒有符合的資料"
      

def select_time(input_time, page = 0):
  cursor = get_database_connection()

  if input_time == "0":
    postgres_select_query = f"""SELECT mountain_name FROM mountain WHERE time_int < 180 LIMIT 9 OFFSET {page}"""
  elif input_time == "1":
    postgres_select_query = f"""SELECT mountain_name FROM mountain WHERE time_int < 360 and time_int >= 180 LIMIT 9 OFFSET {page}"""
  elif input_time == "2":
    postgres_select_query = f"""SELECT mountain_name FROM mountain WHERE time_int < 720 and time_int >= 360 LIMIT 9 OFFSET {page}"""
  elif input_time == "3":
    postgres_select_query = f"""SELECT mountain_name FROM mountain WHERE time_int < 2880 and time_int >= 720 LIMIT 9 OFFSET {page}"""
  elif input_time == "4":
    postgres_select_query = f"""SELECT mountain_name FROM mountain WHERE time_int >= 2880 LIMIT 9 OFFSET {page}"""

  cursor.execute(postgres_select_query)
  ans = cursor.fetchall()
  select = []
  if ans:
    for _ in ans:
      select.append(_[0])
    return select
  else:
      return "很抱歉，沒有符合的資料"
      
import requests
from bs4 import BeautifulSoup
import json
def get_ig_pic(input_location):

  headers = {
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
  'cookie': 'mid=W4VyZwALAAHeINz8GOIBiG_jFK5l; mcd=3; csrftoken=KFLY0ovWwChYoayK3OBZLvSuD1MUL04e; ds_user_id=8492674110; sessionid=IGSCee8a4ca969a6825088e207468e4cd6a8ca3941c48d10d4ac59713f257114e74b%3Acwt7nSRdUWOh00B4kIEo4ZVb4ddaZDgs%3A%7B%22_auth_user_id%22%3A8492674110%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22_auth_user_hash%22%3A%22%22%2C%22_platform%22%3A4%2C%22_token_ver%22%3A2%2C%22_token%22%3A%228492674110%3Avsy7NZ3ZPcKWXfPz356F6eXuSUYAePW8%3Ae8135a385c423477f4cc8642107dec4ecf3211270bb63eec0a99da5b47d7a5b7%22%2C%22last_refreshed%22%3A1535472763.3352122307%7D; csrftoken=KFLY0ovWwChYoayK3OBZLvSuD1MUL04e; rur=FRC; urlgen="{"103.102.7.202": 57695}:1furLR:EZ6OcQaIegf5GSdIydkTdaml6QU"'
  }

  insta_url = f"https://www.instagram.com/explore/tags/{input_location}/"
  res = requests.get(insta_url, headers=headers)

  soup = BeautifulSoup(res.text, "lxml")
  json_part = soup.find_all("script", {"type": "text/javascript"})[3].text[21:-1]

  js_data = json.loads(json_part)
  edges = js_data["entry_data"]['TagPage'][0]["graphql"]['hashtag']['edge_hashtag_to_top_posts']['edges'][0:9]
  urls = []
  for _ in edges:
      url = _['node']['thumbnail_src']
      urls.append(url)
  return urls



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
    bubble = {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "url",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
          "type": "postback",
          "label": "action",
          "data": "pic"
        }
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "山的名稱",
            "weight": "bold",
            "size": "xl"
          },
          {
            "type": "box",
            "layout": "baseline",
            "margin": "md",
            "contents": [
              {
                "type": "text",
                "text": "資訊",
                "size": "sm",
                "margin": "md",
                "flex": 0,
                "weight": "bold"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "區域",
                    "color": "#aaaaaa",
                    "size": "sm",
                    "flex": 1
                  },
                  {
                    "type": "text",
                    "text": "所在地",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "難度",
                    "color": "#aaaaaa",
                    "size": "sm",
                    "flex": 1
                  },
                  {
                    "type": "text",
                    "text": "難度等級",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "距離",
                    "color": "#aaaaaa",
                    "size": "sm",
                    "flex": 1
                  },
                  {
                    "type": "text",
                    "text": "公里數",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "時間",
                    "color": "#aaaaaa",
                    "size": "sm",
                    "flex": 1
                  },
                  {
                    "type": "text",
                    "text": "分鐘小時",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5
                  }
                ]
              }
            ]
          }
        ]
      }
    }
    bubble["hero"]["url"] = picture_url
    bubble["hero"]["action"]["data"] = "pic" + picture_url
    bubble["body"]["contents"][0]["text"] = get_mountain_name(receive)
    bubble["body"]["contents"][2]["contents"][0]["contents"][1]["text"] = get_mountain(receive)[2]
    bubble["body"]["contents"][2]["contents"][1]["contents"][1]["text"] = get_mountain(receive)[3][3:]
    bubble["body"]["contents"][2]["contents"][2]["contents"][1]["text"] = get_mountain(receive)[4]
    bubble["body"]["contents"][2]["contents"][3]["contents"][1]["text"] = get_mountain(receive)[5]
    
    message = FlexSendMessage(alt_text="山的資訊", contents=bubble)
    line_bot_api.reply_message(
        event.reply_token,
        message
    )
  elif receive[:3] == "pic":
    line_bot_api.reply_message(
      event.reply_token,
      ImageSendMessage(
        original_content_url= receive[3:], preview_image_url= receive[3:]
      )
    )

  elif receive[:2] == "ig":
    search = "合歡山"
    urls = get_ig_pic(search)
    line_bot_api.reply_message(
      event.reply_token,
      TextSendMessage(
          text=urls[0]
        )
    )
    # for url in urls:
    #   print(url)
    # all_bubbles_pic = []
    # bubble_pic = {
    #   "type": "bubble",
    #   "size": "kilo",
    #   "hero": {
    #     "type": "image",
    #     "url": "https://instagram.frmq3-2.fna.fbcdn.net/v/t51.2885-15/sh0.08/e35/c0.180.1440.1440a/s640x640/135778407_1304360396589206_6416325874617909960_n.jpg?_nc_ht=instagram.frmq3-2.fna.fbcdn.net&_nc_cat=102&_nc_ohc=Erz9W0tqNVwAX8yx7hC&tp=1&oh=9b4099cd06b1ed2a7fc95b9815223d61&oe=60221A37",
    #     "size": "full",
    #     "aspectMode": "cover",
    #     "aspectRatio": "320:320"
    #   }
    # }
    # all_bubbles_pic.append(bubble_pic)
    # all_bubbles_pic.append(bubble_pic)
    # all_bubbles_pic.append(bubble_pic)

    # bubble_string = {
    #   "type": "carousel",
    #     "contents": all_bubbles_pic
    # }
    # message = FlexSendMessage(
    #   alt_text="圖片輪播", contents=bubble_string
    #   )
    # line_bot_api.reply_message(
    #   event.reply_token,
    #   message
    #   )

  else:
    cmd, seq, page = receive.split()
    page = int(page)
    if cmd == "are":
      print("area_north_east_west_south")
      print("before", page)
      select_list = select_area(seq, page)
      print("after", page)
    elif cmd == "dif":
      print("difficulty")
      print("before", page)
      select_list = select_difficulty(seq, page)
      print("after", page)
    elif cmd == "tim":
      print("time_select")
      print("before", page)
      select_list = select_time(seq, page)
      print("after", page)

    if select_list == "很抱歉，沒有符合的資料":
      print("no_information")
      line_bot_api.reply_message(
          event.reply_token,
          TextSendMessage(
              text=select_list
          )
      )
    elif select_list:
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
      next_page_bubble = {
          "type": "bubble",
          "size": "micro",
          "hero": {
            "type": "image",
            "url": "https://imagizer.imageshack.com/img923/8576/INnfT8.jpg",
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
                "text": "更多資訊",
                "weight": "bold",
                "size": "lg",
                "wrap": True,
              },
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "下9筆資料",
                  "data": cmd + " " + seq + " " + str(page + 9),
                  "displayText": "下9筆資料"
                }
              }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
          }
      }
      print(cmd + seq + str(page))
      all_bubbles.append(next_page_bubble)
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
                    "data": "are 北部 0"
                  },
                  "height": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "postback",
                    "label": "中部",
                    "data": "are 中部 0"
                  },
                  "height": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "postback",
                    "label": "南部",
                    "data": "are 南部 0"
                  },
                  "height": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "postback",
                    "label": "東部",
                    "data": "are 東部 0"
                  },
                  "height": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "postback",
                    "label": "外島",
                    "data": "are 外島 0"
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
                    "data": "dif 0 0"
                  },
                  "height": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "postback",
                    "label": "低-中",
                    "data": "dif 1 0"
                  },
                  "height": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "postback",
                    "label": "中",
                    "data": "dif 2 0"
                  },
                  "height": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "postback",
                    "label": "中-高",
                    "data": "dif 3 0"
                  },
                  "height": "md"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "postback",
                    "label": "高",
                    "data": "dif 4 0"
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
                    "data": "tim 0 0"
                  },
                  "height": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "postback",
                    "label": "3-6小時",
                    "data": "tim 1 0"
                  },
                  "height": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "postback",
                    "label": "6小時-12小時",
                    "data": "tim 2 0"
                  },
                  "height": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "postback",
                    "label": "12小時-兩天",
                    "data": "tim 3 0"
                  },
                  "height": "sm"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "postback",
                    "label": "兩天以上",
                    "data": "tim 4 0"
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
      area_pic_url = "https://imagizer.imageshack.com/img922/3953/FFDfl6.jpg"
      difficulity_pic_url = "https://imagizer.imageshack.com/img924/6579/iRTZcj.jpg"
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
        bubble = {
          "type": "bubble",
          "hero": {
            "type": "image",
            "url": "url",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "action": {
              "type": "postback",
              "label": "action",
              "data": "pic"
            }
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "山的名稱",
                "weight": "bold",
                "size": "xl"
              },
              {
                "type": "box",
                "layout": "baseline",
                "margin": "md",
                "contents": [
                  {
                    "type": "text",
                    "text": "資訊",
                    "size": "sm",
                    "margin": "md",
                    "flex": 0,
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "text",
                        "text": "區域",
                        "color": "#aaaaaa",
                        "size": "sm",
                        "flex": 1
                      },
                      {
                        "type": "text",
                        "text": "所在地",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                      }
                    ]
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "text",
                        "text": "難度",
                        "color": "#aaaaaa",
                        "size": "sm",
                        "flex": 1
                      },
                      {
                        "type": "text",
                        "text": "難度等級",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                      }
                    ]
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "text",
                        "text": "距離",
                        "color": "#aaaaaa",
                        "size": "sm",
                        "flex": 1
                      },
                      {
                        "type": "text",
                        "text": "公里數",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                      }
                    ]
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "text",
                        "text": "時間",
                        "color": "#aaaaaa",
                        "size": "sm",
                        "flex": 1
                      },
                      {
                        "type": "text",
                        "text": "分鐘小時",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                      }
                    ]
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "postback",
                      "label": "更多圖片",
                      "data": "ig_pic",
                      "displayText": "更多圖片"
                    },
                    "position": "relative",
                    "height": "sm"
                  }
                ]
              }
            ]
          }
        }
        bubble["hero"]["url"] = picture_url
        bubble["hero"]["action"]["data"] = "pic" + picture_url
        bubble["body"]["contents"][0]["text"] = get_mountain_name(search)
        bubble["body"]["contents"][2]["contents"][0]["contents"][1]["text"] = get_mountain(search)[2]
        bubble["body"]["contents"][2]["contents"][1]["contents"][1]["text"] = get_mountain(search)[3][3:]
        bubble["body"]["contents"][2]["contents"][2]["contents"][1]["text"] = get_mountain(search)[4]
        bubble["body"]["contents"][2]["contents"][3]["contents"][1]["text"] = get_mountain(search)[5]
        bubble["body"]["contents"][2]["contents"][4]["action"]["data"] = "ig" + search

        message = FlexSendMessage(alt_text="山的資訊", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
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
