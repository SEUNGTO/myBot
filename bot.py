import json
import os
import requests

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
THEME_URL = os.getenv('THEMES_JSON_URL')


def get_theme(stock_code):
    # GitHub에서 테마 데이터 가져오기
    response = requests.get(THEME_URL)  # 저장소 URL을 실제로 사용하는 URL로 수정해주세요.
    themes = json.loads(response.text)

    # 종목 코드로 테마 찾기
    theme = themes.get(stock_code, "테마를 찾을 수 없습니다.")
    return theme


def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, params=params)


def main():

    chat_id = os.getenv('CHAT_ID')
    message_text = os.getenv('MESSAGE_TEXT')

    if message_text.startswith("/theme"):
        stock_code = message_text.split()[-1]
        theme = get_theme(stock_code)
        send_message(chat_id, f"{stock_code} 종목의 테마는 '{theme}'입니다.")


if __name__ == "__main__":
    main()
