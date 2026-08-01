import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://rozetka.com.ua/ua/search/?text=пиво%2024"

LIMIT = 700


def send(text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text
        }
    )


headers = {
    "User-Agent": "Mozilla/5.0"
}

page = requests.get(URL, headers=headers)
print(page.status_code)

soup = BeautifulSoup(page.text, "html.parser")
print(page.text[:1000])

found = False

for item in soup.find_all("span"):

    text = item.get_text(strip=True)

    if text.endswith("₴"):

        price = "".join(ch for ch in text if ch.isdigit())

        if price:

            price = int(price)

            if price <= LIMIT:

                send(f"🍺 Знайдено пиво за {price} грн!\n{URL}")

                found = True

                break

if not found:
    send("Нічого дешевше 700 грн не знайдено.")