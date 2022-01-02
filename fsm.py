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

year = []
time = []
rating = []

rand = 0
types = ''
search_str = ''

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
movie_data = soup.findAll('div', attrs={'class': 'lister-item mode-advanced'})

for store in movie_data:
    movie_dic = {'name': store.h3.a.text,
                 'year': store.h3.find('span', class_='lister-item-year text-muted unbold').text,
                 'time': store.p.find('span', class_='runtime').text,
                 'rating': store.find('div', class_='inline-block ratings-imdb-rating').text.replace('\n', ''),
                 'votes': '', 'gross': '', 'genre': '', 'intro': '', 'img': ''}
    value = store.find_all('span', attrs={'name': 'nv'})

    imageDiv = store.find('div', {'class': 'lister-item-image float-left'})
    movie_dic['img'] = img = imageDiv.a.img['loadlate']

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

        global rand
        rand = random.randint(0, len(movie_dic_array))
        my_url = movie_dic_array[rand]['img']
        text = 'name: ' + movie_dic_array[rand]['name'] + ' 這部怎樣?'
        # text += 'year: ' + movie_dic_array[rand]['year'] + '\n'
        # text += 'genre: ' + movie_dic_array[rand]['rating'] + '\n'
        # text += 'time: ' + movie_dic_array[rand]['time'] + '\n'
        # text += 'rating: ' + movie_dic_array[rand]['rating'] + '\n'
        # text += 'votes: ' + movie_dic_array[rand]['votes'] + '\n'
        # text += 'gross: ' + movie_dic_array[rand]['gross'] + '\n'
        # text += movie_dic_array[0]['intro']
        btn = [
            MessageTemplateAction(
                label='謝了 這不錯 我要看細節',
                text='謝了 這不錯 我要看細節'
            ),
            MessageTemplateAction(
                label='再隨機推薦',
                text='隨機推薦'
            ),
        ]
        # push_message(event.reply_token,text)
        send_button_message(event.reply_token, title, text, btn, my_url)

    def is_going_to_randomDetail(self, event):
        text = event.message.text
        return text.lower() == "謝了 這不錯 我要看細節"

    def on_enter_randomDetail(self, event):
        yourMovie = 'name: ' + movie_dic_array[rand]['name'] + '\n'
        yourMovie += 'year: ' + movie_dic_array[rand]['year'] + '\n'
        yourMovie += 'genre: ' + movie_dic_array[rand]['rating'] + '\n'
        yourMovie += 'time: ' + movie_dic_array[rand]['time'] + '\n'
        yourMovie += 'rating: ' + movie_dic_array[rand]['rating'] + '\n'
        yourMovie += 'votes: ' + movie_dic_array[rand]['votes'] + '\n'
        yourMovie += 'gross: ' + movie_dic_array[rand]['gross'] + '\n'
        # yourMovie += 'img: ' + movie_dic_array[rand]['img'] + '\n'
        yourMovie += movie_dic_array[rand]['intro']

        send_text_message(event.reply_token, yourMovie)
        self.go_back()

    def is_going_to_all(self, event):
        text = event.message.text
        return text.lower() == "all"

    def on_enter_all(self, event):
        str = ""
        print("I'm entering all")

        for movie in movie_dic_array:
            str += movie['name'] + "\n"
        global types
        types = ''
        str += '----請輸入一個你想看的----'
        send_text_message(event.reply_token, str)

    def is_going_to_crime(self, event):
        text = event.message.text
        return text.lower() == "crime"

    def on_enter_crime(self, event):
        global search_str
        search_str = ""
        print("I'm entering all")

        for movie in movie_dic_array:
            if 'crime' in movie['genre'].lower():
                search_str += movie['name'] + "\n"
        global types
        types = 'crime'
        search_str += '----請輸入一個你想看的----'
        send_text_message(event.reply_token, search_str)

    def is_going_to_romance(self, event):
        text = event.message.text
        return text.lower() == "romance"

    def on_enter_romance(self, event):
        global search_str
        search_str = ""
        print("I'm entering all")

        for movie in movie_dic_array:
            if 'romance' in movie['genre']:
                search_str += movie['name'] + "\n"
        global types
        types = 'romance'
        search_str += '----請輸入一個你想看的----'
        send_text_message(event.reply_token, search_str)

    def is_going_to_intro(self, event):
        text = event.message.text

        global search_str
        search_str = text
        for movie in movie_dic_array:
            if types in movie['genre']:
                if movie['name'].lower() == text.lower():
                    return True
        # return text.lower() in search_str.lower()

    def on_enter_intro(self, event):
        print("intro=========================")
        for movie in movie_dic_array:
            if movie['name'].lower() == search_str.lower():
                search_movie = 'name: ' + movie['name'] + '\n'
                search_movie += 'year: ' + movie['year'] + '\n'
                search_movie += 'genre: ' + movie['rating'] + '\n'
                search_movie += 'time: ' + movie['time'] + '\n'
                search_movie += 'rating: ' + movie['rating'] + '\n'
                search_movie += 'votes: ' + movie['votes'] + '\n'
                search_movie += 'gross: ' + movie['gross'] + '\n'
                search_movie += movie['intro']
                send_text_message(event.reply_token, search_movie)
                break
        #send_text_message(event.reply_token, search_movie)
        self.go_back()
