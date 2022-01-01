import string

import requests
from transitions.extensions import GraphMachine

import myMessage
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

    def is_going_to_user(self, event):
        text = event.message.text
        return text.lower() =="I don't have time" or text.lower() =="謝了 這不錯"   #



    def is_going_to_menu(self, event):
        text = event.message.text
        return text.lower() == "menu"  # user to state1

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
        line_bot_api.push_message(event.reply_token, TextSendMessage(text=message))


    def is_going_to_random(self, event):
        text = event.message.text
        return text.lower() == "推薦隨機"  #

    def on_enter_random(self, event):  # when enter state1
        print("I'm entering random")
        title = '滿意嗎？'
        text="efefefesfsefesfsfsfsdfdsfsdfdsfdsf" \
             "dfgsdfsdfsdfsdfsfdvflvfllvlv" \
             "hjikiki,kmjmjmjmhmhjmjhmjhm"
        btn = [
            MessageTemplateAction(
                label='謝了 這不錯',
                text='謝了 這不錯'
            ),
            MessageTemplateAction(
                label='推薦隨機',
                text='推薦隨機'
            ),
        ]

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
