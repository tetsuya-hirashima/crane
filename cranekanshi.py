import os
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# LINE Notifyのアクセストークン
ACCESS_TOKEN = "YolFJkMrCYO5jOcjAjaiOBqqAV8iFP2mRfXHVztB3Ni"
LINE_API = "https://notify-api.line.me/api/notify"

# WebDriverの設定・取得
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1024,768')

    # Webdriver ManagerでChromeDriverを取得
    driver = webdriver.Chrome(
        executable_path=ChromeDriverManager().install(),
        options=options)
    driver.set_page_load_timeout(15)
    driver.implicitly_wait(15)
    return driver

# 結果をLINEへ送信
def notify_to_line(message, image_file_path=None):
    headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN}
    payload = {'message': message}
    files = {}
    if ((image_file_path is not None) and os.path.exists(image_file_path)):
        files = {'imageFile': open(image_file_path, 'rb')}

    response = requests.post(LINE_API, headers=headers, params=payload, files=files)

def main():
    driver = get_driver()
    driver.get('https://www.rsv-crane.jp/login')
    driver.save_screenshot('qiita.png')
    # テキストのみ送信
    notify_to_line('チェック結果')
    # テキスト + 画像を送信
    notify_to_line('スクリーンショット', 'qiita.png')
    driver.close()
    driver.quit()

if __name__ == "__main__":
    main()
