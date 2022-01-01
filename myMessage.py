from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
from utils import *
# import pandas as pd
import requests

# from bs4 import BeautifulSoup
# moviesDB = imdb.IMDb()
# movies = moviesDB.search_movie('')



chooseTypes = {
    "type": "carousel",
    "contents": [
        {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://i.imgur.com/qyJCDS8.jpg",
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "1.25:2"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "All",
                            "text": "All"
                        },
                        "color": "#9620a4",
                        "height": "md",
                        "style": "primary",
                        "offsetBottom": "md"
                    }
                ],
                "spacing": "lg"
            }
        },
        {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://i.imgur.com/XflSTSP.jpg",
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "1.25:2"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "Crime",
                            "text": "crime"
                        },
                        "height": "md",
                        "color": "#c98938",
                        "style": "primary",
                        "offsetBottom": "md"
                    }
                ],
                "spacing": "lg"
            }
        },
        {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://i.imgur.com/SM9qBsm.jpg",
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "1.25:2",
                "backgroundColor": "#d5a6bd"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "Romance",
                            "text": "romance"
                        },
                        "height": "md",
                        "color": "#d5a6bd",
                        "style": "primary",
                        "offsetBottom": "md"
                    }
                ],
                "spacing": "lg"
            }
        },
        {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://i.imgur.com/DWdNRSU.jpg",
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "1.25:2"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "Adventure",
                            "text": "adventure"
                        },
                        "height": "md",
                        "color": "#00b4b4",
                        "style": "primary",
                        "offsetBottom": "md"
                    }
                ],
                "spacing": "lg"
            }
        },
        {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://i.imgur.com/7Dz1JTm.jpg",
                "aspectRatio": "1.25:2",
                "size": "full",
                "aspectMode": "cover"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "Action",
                            "text": "action"
                        },
                        "offsetBottom": "md",
                        "color": "#541d8b",
                        "height": "md",
                        "style": "primary"
                    }
                ]
            }
        },
        {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://i.imgur.com/AEFInPK.jpg",
                "size": "full",
                "aspectRatio": "1.25:2",
                "aspectMode": "cover"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "Fantasy",
                            "text": "fantasy"
                        },
                        "offsetBottom": "md",
                        "style": "primary",
                        "height": "md",
                        "color": "#2f3c56"
                    }
                ]
            }
        },
        {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://i.imgur.com/kQHDPql.jpg",
                "size": "full",
                "aspectRatio": "1.25:2",
                "aspectMode": "fit"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "Biography",
                            "text": "biography"
                        },
                        "style": "primary",
                        "height": "md",
                        "offsetBottom": "md",
                        "color": "#929fd1"
                    }
                ]
            }
        }
    ]
}
