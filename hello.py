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
def picture(event):
    import os
    import psycopg2

    DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a rocky-brushlands-15389').read()[:-1]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    create_table_query = '''CREATE TABLE mountain(
        mountain_id serial PRIMARY KEY,
        mountain_name VARCHAR (50) UNIQUE NOT NULL,
        area VARCHAR (50) NOT NULL,
        difficulty VARCHAR (50) NOT NULL,
        time VARCHAR (50) NOT NULL,
        type VARCHAR (50) NOT NULL
    );'''
        
    cursor.execute(create_table_query)
    conn.commit()

    import requests
    from bs4 import BeautifulSoup

    url = "https://hiking.biji.co/index.php?q=trail"

    re = requests.get(url)
    soup = BeautifulSoup(re.text, 'html.parser')

    table = soup.find('div', {'id': 'trail_list'})
    #print(table)
    data = []
    mountain = []
    for trail in table.find_all('div', {'class': "pic-item"}):
        #print(trail)
        
        name = trail.a['title']
        location = trail.find('div', {'class': 'location'}).text
        info = trail.find_all('li', {'class': "search-info-item"})
        info_lst = [i.text for i in info]
        mountain = []
        mountain.append(name)
        mountain.append(location)
        mountain.append(info_lst[0])
        mountain.append(info_lst[1])
        mountain.append(info_lst[2])
        mountain = tuple(mountain)
        data.append(mountain)

    print(data)

    import os
    import psycopg2

    DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a rocky-brushlands-15389').read()[:-1]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()


    table_columns = '(mountain_name, area, difficulty, time, type)'
    postgres_insert_query = f"""INSERT INTO mountain {table_columns} VALUES (%s, %s, %s, %s, %s);"""

    cursor.executemany(postgres_insert_query, data)
    conn.commit()

    count = cursor.rowcount

    print(count, "Record inserted successfully into alpaca_training")

    cursor.close()
    conn.close()

    import os
    import psycopg2

    DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a rocky-brushlands-15389').read()[:-1]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    postgres_select_query = f"""SELECT * FROM mountain"""

    cursor.execute(postgres_select_query)

    text = cursor.fetchall()
    
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text = event.message.text))
        print("line bot")
    except:
        print("mack sure the func activite into except")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = event.message.text)
        )
        pass






if __name__ == "__main__":
    app.run()

