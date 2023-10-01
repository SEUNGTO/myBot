import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = 'YOUR_BOT_TOKEN'
URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
THEMES_URL = 'https://raw.githubusercontent.com/SEUNGTO/botdata/main/themes.json'

def get_themes_from_github(stock_code):
    response = requests.get(THEMES_URL)
    themes_data = response.json()
    return themes_data.get(stock_code, [])

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.json
    chat_id = update['message']['chat']['id']
    text = update['message']['text']

    if text.startswith('/theme'):
        command, stock_code = text.split(' ', 1)
        themes = get_themes_from_github(stock_code)

        if themes:
            theme_message = f"The themes for {stock_code} are: {', '.join(themes)}"
        else:
            theme_message = f"No themes found for {stock_code}"

        requests.post(URL, json={'chat_id': chat_id, 'text': theme_message})

    return 'OK'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)