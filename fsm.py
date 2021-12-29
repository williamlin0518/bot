import string

import requests
from transitions.extensions import GraphMachine

from utils import *
from bs4 import BeautifulSoup

location = ""
url = 'https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating'


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "1"  # user to state1

    def on_enter_state1(self, event):  # when enter state1
        print("I'm entering state1")

        title = '看啥電影'
        text = '科幻？ 浪漫？'
        btn = [
            MessageTemplateAction(
                label='科幻',
                text='科幻'
            ),
            MessageTemplateAction(
                label='浪漫',
                text='浪漫'
            ),
        ]
        url = 'https://i.imgur.com/8Vvxj0S.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "科幻"

    def on_enter_state2(self, event):
        print("I'm entering state2")
        response = requests.get(url)

        # BeautifulSoup(response.content, 'html.parser')
        # soup = BeautifulSoup(response.content, 'html.parser')
        # souptext = soup[0:400]
        send_text_message(event.reply_token, "state2")

    def on_exit_state2(self):
        print("Leaving state2")
