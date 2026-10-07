import sys
from reddit_monitor import start_monitor
from telegram_bot import send_message

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


if __name__ == "__main__":
    send_message(
        "🚨 RAILWAY TEST\n\n"
        "Crypto Reddit Alert Bot is running successfully on Railway."
    )

    start_monitor()