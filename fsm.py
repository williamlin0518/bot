import string

import requests
import random
from transitions.extensions import GraphMachine

import myMessage
from utils import *
from bs4 import BeautifulSoup

location = ""
url = 'https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating'

movie_dic_array = []
movie_dic = {
    'name': '',
    'year': '',
    'time': '',
    'rating': '',
    'votes': '',
    'gross': '',

    'genre': '',
    'intro': ''
}

movie_name = []
year = []
time = []
rating = []

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
movie_data = soup.findAll('div', attrs={'class': 'lister-item mode-advanced'})

for store in movie_data:
    movie_dic['movie_name'] = store.h3.a.text
    movie_dic['year'] = store.h3.find('span', class_='lister-item-year text-muted unbold').text
    movie_dic['time'] = store.p.find('span', class_='runtime').text
    movie_dic['rating'] = store.find('div', class_='inline-block ratings-imdb-rating').text.replace('\n', '')

    value = store.find_all('span', attrs={'name': 'nv'})
    movie_dic['votes'] = value[0].text
    movie_dic['gross'] = value[1].text if len(value) > 1 else 'No data'
    movie_dic['genre'] = store.p.find('span', class_='genre').text
    movie_dic['intro'] = store.find_all('p', {'class': 'text-muted'})[1].text
    movie_dic_array.append(movie_dic)


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_menu(self, event):
        text = event.message.text
        return text.lower() == "menu" or "I don't have time" or text.lower() == "謝了 這不錯"  # user to state1

    def on_enter_menu(self, event):  # when enter state1
        print("I'm entering menu")

        title = '要做什麼呢？'
        text = '可幫你找電影、隨機推薦、看fsm圖'
        btn = [
            MessageTemplateAction(
                label='想找電影',
                text='想找電影'
            ),
            MessageTemplateAction(
                label='隨機推薦',
                text='隨機推薦'
            ),
            MessageTemplateAction(
                label='看fsm圖',
                text='看fsm圖'
            ),
            MessageTemplateAction(
                label="I don't have time",
                text="I don't have time"
            ),
        ]
        url = 'https://i.imgur.com/8Vvxj0S.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_whichKind(self, event):
        text = event.message.text
        return text.lower() == "想找電影"  #

    def on_enter_whichKind(self, event):  # when enter whichKind
        print("in whichKind")
        message = myMessage.chooseTypes

        message_to_reply = FlexSendMessage("選種類", message)

        line_bot_api = LineBotApi(channel_access_token)
        line_bot_api.reply_message(event.reply_token, message_to_reply)

    def is_going_to_random(self, event):
        text = event.message.text
        return text.lower() == "隨機推薦"  #

    def on_enter_random(self, event):  # when enter state1
        print("I'm entering random")
        title = '滿意嗎？'

        rand = random.randint(0, len(movie_dic_array))
        text = 'name: ' + movie_dic_array[rand]['name'] + '\n'
        text += 'year: ' + movie_dic_array[rand]['year'] + '\n'
        text += 'genre: ' + movie_dic_array[rand]['rating'] + '\n'
        text += 'time: ' + movie_dic_array[rand]['time'] + '\n'
        text += 'rating: ' + movie_dic_array[rand]['rating'] + '\n'
        text += 'votes: ' + movie_dic_array[rand]['votes'] + '\n'
        text += 'gross: ' + movie_dic_array[rand]['gross'] + '\n'

        # text += movie_dic_array[0]['intro']

        btn = [
            MessageTemplateAction(
                label='謝了 這不錯',
                text='謝了 這不錯'
            ),
            MessageTemplateAction(
                label='隨機推薦',
                text='隨機推薦'
            ),
        ]

        send_button_message(event.reply_token, title, '123', btn, url)
        send_text_message(event.reply_token, text)

    def is_going_to_all(self, event):
        text = event.message.text
        return text.lower() == "科幻"

    def on_enter_all(self, event):
        str = ""
        print("I'm entering all")

        for store in movie_data:
            name = store.h3.a.text
            runtime = store.p.find('span', class_='runtime').text

            str += name
            str += " "
            str += store.h3.find('span', class_='lister-item-year text-muted unbold')
            str += runtime

            str += " \n"

        send_text_message(event.reply_token, str)

        self.go_back()

    def on_exit_state2(self):
        print("Leaving state2")
