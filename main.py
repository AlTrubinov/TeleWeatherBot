import requests
import json
import const
import telebot
from telebot import types

bot = telebot.TeleBot(const.TOKEN, parse_mode=None)


def parse_weather_data(types, data):
    if types == 'weather1':
        for elem in data['weather']:
            weather_state = elem['main']
        temp = data['main']['temp']
        city = data['name']
        msg = f'The weather in {city} is {temp}° degree. State is {weather_state}.'
    elif types == 'weather24':
        city = data['city']['name']
        msg = f'The weather in {city} for 24 hours (GMT+7):\n'
        for elem in data['list']:
            date_time = elem['dt_txt']
            temp = elem['main']['temp']
            for weath_elem in elem['weather']:
                weather_state = weath_elem['main']
            msg += f'{date_time}: Temp is {temp}°.\nState is {weather_state}.\n\n'

    return msg


def get_weather(types, location):
    url = const.WEATHER_URL[types].format(city=location, token=const.WEATHER_TOKEN)
    response = requests.get(url)
    if response.status_code != 200:
        return 'City not found. Try again or send another city.'
    data = json.loads(response.content)
    return parse_weather_data(types, data)


@bot.message_handler(commands=['start', 'help', 'info'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "Hi, I'm weather bot, you can send me any city and I will tell you about the weather in it!")


@bot.message_handler(content_types=['text'])
def get_message(message):
    city = message.text
    weather_types = types.InlineKeyboardMarkup()
    weather_btn1 = types.InlineKeyboardButton(text='Weather right now', callback_data=f'weather1 {city}')
    weather_btn5 = types.InlineKeyboardButton(text='Weather for 24 hours', callback_data=f'weather24 {city}')
    weather_types.add(weather_btn1, weather_btn5)
    bot.send_message(message.chat.id, "Now choose what you need", reply_markup=weather_types)


@bot.callback_query_handler(func=lambda m: True)
def answer(call):
    answer = str(call.data).split()
    if answer[0] == 'weather1':
        bot.send_message(call.message.chat.id, get_weather(answer[0], answer[1]))
    elif answer[0] == 'weather24':
        bot.send_message(call.message.chat.id, get_weather(answer[0], answer[1]))


bot.polling(none_stop=True, interval=0)
