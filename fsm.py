import string

import requests
from transitions.extensions import GraphMachine

from utils import *
from bs4 import BeautifulSoup

location = ""
url = 'https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating'

movie_dic_array = []
movie_dic = {
    'name': '',
    'year': 0,
    'time': 0,
    'rating': 0,
    'metascore': 0,
    'votes': 0,
    'gross': '',
    'intro':''
}


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_menu(self, event):
        text = event.message.text
        return text.lower() == "想看電影了"  # user to state1

    def on_enter_menu(self, event):  # when enter state1
        print("I'm entering menu")

        title = '喜歡哪種電影'
        text = 'Crime? Romance? Adventure? Action? Biography? Fantasy?'
        btn = [
            MessageTemplateAction(
                label='All',
                text='All'
            ),
            MessageTemplateAction(
                label='Crime',
                text='Crime'
            ),
            MessageTemplateAction(
                label='Romance',
                text='Romance'
            ),
            MessageTemplateAction(
                label='Adventure',
                text='Adventure'
            ),
            MessageTemplateAction(
                label='Action',
                text='Action'
            ),
            MessageTemplateAction(
                label='Biography',
                text='Biography'
            ),
            MessageTemplateAction(
                label='Fantasy',
                text='Fantasy'
            ),
            MessageTemplateAction(
                label="I don't have time",
                text="I don't have time"
            ),
        ]
        url = 'https://i.imgur.com/8Vvxj0S.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_random(self, event):
        text = event.message.text
        return text.lower() == "推薦隨機"  #

    def on_enter_random(self, event):  # when enter state1
        print("I'm entering random")
        title = '滿意嗎？'
        text=""
        btn = [
            MessageTemplateAction(
                label='謝了 這不錯',
                text='謝了 這不錯'
            ),
            MessageTemplateAction(
                label='再推薦隨機',
                text='再推薦隨機'
            ),
        ]
        send_button_message(event.reply_token, title, text, btn, url)
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_all(self, event):
        text = event.message.text
        return text.lower() == "科幻"

    def on_enter_all(self, event):
        print("I'm entering all")
        response = requests.get(url)
        movie_name = []
        year = []
        time = []
        rating = []
        metascore = []
        votes = []
        gross = []
        char_number = 0
        str = ""
        soup = BeautifulSoup(response.content, 'html.parser')
        movie_data = soup.findAll('div', attrs={'class': 'lister-item mode-advanced'})

        for store in movie_data:
            name = store.h3.a.text
            runtime = store.p.find('span', class_='runtime').text
            char_number += len(name)
            # if char_number > 100:
            #     break
            str += name
            str += " "
            str += store.h3.find('span', class_='lister-item-year text-muted unbold')
            str += runtime

            str += " \n"

        send_text_message(event.reply_token, str)

        self.go_back()

    def on_exit_state2(self):
        print("Leaving state2")
