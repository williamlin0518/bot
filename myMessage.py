from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
from utils import *
import imdb
location = ""
def massage_handler(input, line_bot_api, event):
    if '看電影' in input:
        message = imagemap_message()
        # send_text_message(event.reply_token, ["請點選你要去哪看", message])
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text="請點選你要去哪看"), message])

    elif '功能' in input:

        send_text_message(event.reply_token, "輸入 看電影\n"
                                             "了解電影")
    else:
        message = TextSendMessage(text=input)
        line_bot_api.reply_message(event.reply_token, message)


# ImagemapSendMessage(組圖訊息)
def imagemap_message():
    message = ImagemapSendMessage(
        base_url="https://i.imgur.com/8Vvxj0S.jpg",
        alt_text='去哪看？',
        base_size=BaseSize(height=1000, width=1000),
        actions=[
            URIImagemapAction(
                # 台南國賓影城
                link_uri="https://tw.shop.com/search/%E5%AE%B6%E6%A8%82%E7%A6%8F",
                area=ImagemapArea(
                    x=0, y=0, width=500, height=500
                )
            ),
            URIImagemapAction(
                # 台南南紡威秀影城
                link_uri="https://tw.shop.com/search/%E7%94%9F%E6%B4%BB%E5%B8%82%E9%9B%86",
                area=ImagemapArea(
                    x=500, y=0, width=500, height=500
                )
            ),
            URIImagemapAction(
                # 台南FOCUS威秀影城
                link_uri="https://tw.shop.com/search/%E9%98%BF%E7%98%A6%E7%9A%AE%E9%9E%8B",
                area=ImagemapArea(
                    x=0, y=500, width=500, height=500
                )
            ),
            URIImagemapAction(
                # 台南大遠百威秀影城
                link_uri="https://tw.shop.com/search/%E5%A1%94%E5%90%89%E7%89%B9",
                area=ImagemapArea(
                    x=500, y=500, width=500, height=500
                )
            )

        ]
    )
    return message
