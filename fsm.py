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
        return text.lower() == "想看電影了"  # user to state1

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
        movie_name = []
        char_number = 0
        str = ""
        soup = BeautifulSoup(response.content, 'html.parser')
        movie_data = soup.findAll('div', attrs={'class': 'lister-item mode-advanced'})

        for store in movie_data:
            name = store.h3.a.text
            char_number += len(name)
            # if char_number > 100:
            #     break
            str += name


        send_text_message(event.reply_token,str )

        self.go_back()

    def on_exit_state2(self):
        print("Leaving state2")
