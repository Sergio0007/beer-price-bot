import os
import requests
from playwright.sync_api import sync_playwright

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://rozetka.com.ua/ua/search/?text=пиво%2024"


def send(text):
    if BOT_TOKEN and CHAT_ID:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": text
            }
        )


with sync_playwright() as p:

    browser = p.chromium.launch(
        executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled"
        ]
    )

    page = browser.new_page()

    page.goto(URL, wait_until="domcontentloaded", timeout=60000)

    # Чекаємо повного завантаження
    page.wait_for_timeout(5000)

    print("Заголовок сторінки:")
    print(page.title())

    # Зберігаємо HTML
    with open("rozetka.html", "w", encoding="utf-8") as f:
        f.write(page.content())

    print("✅ Файл rozetka.html збережено!")

    input("Натисни Enter для завершення...")

    browser.close()

send("HTML успішно збережено!")