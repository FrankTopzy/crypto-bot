from reddit_monitor import start_monitor
from telegram_bot import send_message


if __name__ == "__main__":
    send_message(
        "🚨 RAILWAY TEST\n\n"
        "Crypto Reddit Alert Bot is running successfully on Railway."
    )

    start_monitor()