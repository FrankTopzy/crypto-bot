import requests

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def send_message(message):
    url = (
        f"https://api.telegram.org/"
        f"bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    )

    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
    }

    try:
        response = requests.post(
            url,
            json=data,
            timeout=20
        )

        result = response.json()

        if not result.get("ok"):
            print(f"[WARNING] Telegram API error: {result}")
        else:
            print("[OK] Telegram message sent successfully.")

        return result

    except requests.exceptions.RequestException as error:
        print(f"❌ Failed to send Telegram message: {error}")
        return None