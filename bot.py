import json
import requests

TOKEN = 'YOUR_BOT_TOKEN'
URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
THEMES_URL = 'https://raw.githubusercontent.com/SEUNGTO/botdata/main/themes.json'

def send_message(chat_id, text):
    params = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(URL, params=params)


def get_theme(stock_code):
    response = requests.get(THEMES_URL)
    themes_data = response.json()
    return themes_data.get(stock_code, [])

def main():
    update = json.loads(input())
    chat_id = update["message"]["chat"]["id"]
    message_text = update["message"]["text"]

    if message_text.startswith("/theme"):
        stock_code = message_text.split()[-1]
        theme = get_theme(stock_code)
        send_message(chat_id, f"{stock_code} 종목의 테마는 '{theme}'입니다.")


if __name__ == '__main__':
    main()