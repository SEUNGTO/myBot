import requests
import os

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
URL = f'https://api.telegram.org/bot{TOKEN}/getUpdates'
THEMES_URL = os.getenv('THEMES_JSON_URL')

offset = None

# git test

def get_themes_from_github(stock_code):

    response = requests.get(THEMES_URL)
    themes_data = response.json()
    return themes_data.get(stock_code, [])

while True:
    params = {'offset': offset, 'timeout': 30}
    response = requests.get(URL, params=params)
    messages = response.json().get('result', [])

    for message in messages:
        offset = message['update_id'] + 1
        chat_id = message['message']['chat']['id']
        text = message['message']['text']

        if text.startswith('/theme'):
            command, stock_code = text.split(' ', 1)
            themes = get_themes_from_github(stock_code)

            if themes:
                theme_message = f"The themes for {stock_code} are: {', '.join(themes)}"
            else:
                theme_message = f"No themes found for {stock_code}"

            requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage',
                          json={'chat_id': chat_id, 'text': theme_message})
