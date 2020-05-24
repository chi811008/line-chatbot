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


@handler.add(PostbackEvent)
def handle_post_message(event):
# can not get event text
    print("event =", event)
    line_bot_api.reply_message(
                event.reply_token,
                TextMessage(
                    text=str(str(event.postback.data)),
                )
            )


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event =", event)
    if event.message.text == "查詢個人檔案":
        user_id = event.source.user_id
        profile = line_bot_api.get_profile(user_id, timeout=None)
        line_bot_api.reply_message(
                    event.reply_token,
                    TextMessage(
                        text=str(profile),
                    )
                )

    elif event.message.text == "buttons":
        button_template_message =ButtonsTemplate(
                                thumbnail_image_url="https://i.imgur.com/eTldj2E.png?1",
                                title='Menu',
                                text='Please select',
                                image_size="cover",
                                actions=[
    #                                PostbackTemplateAction 點擊選項後，
    #                                 除了文字會顯示在聊天室中，
    #                                 還回傳data中的資料，可
    #                                 此類透過 Postback event 處理。
                                    PostbackTemplateAction(
                                        label='查詢個人檔案顯示文字-Postback',
                                        text='查詢個人檔案',
                                        data='action=buy&itemid=1'
                                    ),
                                    PostbackTemplateAction(
                                        label='不顯示文字-Postback',
                                        text = None,
                                        data='action=buy&itemid=1'
                                    ),
                                    MessageTemplateAction(
                                        label='查詢個人檔案-Message', text='查詢個人檔案'
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
    elif event.message.text == "carousel":
        image_url_1 = "https://i.imgur.com/eTldj2E.png?1"
        image_url_2 = "https://i.imgur.com/mB9yDO0.png"
        click_link_1 = "https://www.facebook.com/ntustcc"
        click_link_2 = "https://www.facebook.com/ntustcc"
        carousel_template = template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url=image_url_1,
                            title='template-1',
                            text='text-1',
                            actions=[
                                PostbackTemplateAction(
                                    label='postback-1',
                                    text='postback text1',
                                    data='result=1'
                                ),
                                MessageTemplateAction(
                                    label='message-1',
                                    text='message text1'
                                ),
                                URITemplateAction(
                                    label='uri-1',
                                    uri=click_link_1
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url=image_url_2,
                            title='template-2',
                            text='text-2',
                            actions=[
                                PostbackTemplateAction(
                                    label='postback-2',
                                    text='postback text2',
                                    data='result=2'
                                ),
                                MessageTemplateAction(
                                    label='message-2',
                                    text='message text2'
                                ),
                                URITemplateAction(
                                    label='link-2',
                                    uri=click_link_2
                                )
                            ]
                        )]
                    )
        try:
        #     alt_text 因template只能夠在手機上顯示，因此在PC版會使用alt_Text替代
            line_bot_api.push_message(to, TemplateSendMessage(alt_text="Carousel Template Example", template=carousel_template))
        except LineBotApiError as e:
            # error handle
            raise e
        
    
    else:
        line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=11539, sticker_id=52114113))

@app.route('/')
def homepage():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run()
