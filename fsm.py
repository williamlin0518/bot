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

        return text.lower() == "1"

    def is_going_to_state2(self, event):
        response = requests.get(url)
        soup = BeautifulSoup(response.content,'html.parser')
        send_text_message(event.reply_token, soup)
        text = event.message.text
        return text.lower() == "2"

    def on_enter_state1(self, event):
        print("I'm entering state1")

        title = '看啥電影'
        text = '科幻？ 浪漫？'
        btn = [
            MessageTemplateAction(
                label='科幻',
                text='？？'
            ),
            MessageTemplateAction(
                label='浪漫',
                text='？？'
            ),
        ]
        url = 'https://i.imgur.com/8Vvxj0S.jpg'
        send_button_message(event.reply_token, title, text, btn, url)




    def on_exit_state1(self):
        print("Leaving state1")

    def on_enter_state2(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state2")
        self.go_back()

    def on_exit_state2(self):
        print("Leaving state2")
