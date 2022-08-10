from flask import Flask
from flask import request
from flask import jsonify
import requests
import json
import const
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)


def write_json(data, filename='answer.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def send_message(chat_id, text='Nothing city'):
    url = const.URL.format(TOKEN=const.TOKEN, method=const.send_method)
    data = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=data)
    return response.json()


def parse_weather_data(data):
    for elem in data['weather']:
        weather_state = elem['main']
    temp = round(data['main']['temp'], 2)
    city = data['name']
    msg = f'The weather in {city} is {temp}° degree. State is {weather_state}.'
    return msg


def get_weather(location):
    url = const.WEATER_URL.format(city=location, token=const.WEATHER_TOKEN)
    response = requests.get(url)
    if response.status_code != 200:
        return 'City not found. Try again or send another city.'
    data = json.loads(response.content)
    return parse_weather_data(data)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        response = request.get_json()
        chat_id = response['message']['chat']['id']
        message = response['message']['text']
        if message in ['/start', '/help']:
            help_text = "Hi, I'm weather bot, you can send me any city and I will tell you about the weather in it! " \
                        "But if I do not know such a city, you will see the following message:"
            send_message(chat_id=chat_id, text=help_text)

        msg = get_weather(message)
        send_message(chat_id=chat_id, text=msg)
        write_json(response)
        return jsonify(response)
    return '<h1>Welcome from bot</h1>'


if __name__ == '__main__':
    app.run()
