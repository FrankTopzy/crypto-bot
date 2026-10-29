import sys
import os
import threading
import time
from flask import Flask, jsonify

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from reddit_monitor import start_monitor
from telegram_bot import send_message

web_app = Flask(__name__)

# Track bot status for the /health endpoint
bot_status = {
    "running": False,
    "started_at": None,
    "last_error": None,
    "crash_count": 0,
}


@web_app.route("/")
def home():
    return "Bot is running!"


@web_app.route("/health")
def health():
    return jsonify(bot_status)


def run_monitor():
    """Run the Reddit monitor with automatic crash recovery."""
    bot_status["running"] = True
    bot_status["started_at"] = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())

    while True:
        try:
            start_monitor()
        except Exception as e:
            bot_status["crash_count"] += 1
            bot_status["last_error"] = f"{type(e).__name__}: {e}"
            error_msg = (
                "⚠️ BOT CRASHED & RESTARTING\n\n"
                f"Error: {type(e).__name__}: {e}\n"
                f"Crash count: {bot_status['crash_count']}\n"
                f"Restarting in 30 seconds..."
            )
            print(error_msg)
            try:
                send_message(error_msg)
            except Exception:
                pass
            time.sleep(30)


if __name__ == "__main__":
    # Send startup notification so you know the bot is alive
    try:
        result = send_message("✅ Bot started successfully on Render!")
        if result and result.get("ok"):
            print("[OK] Startup Telegram test passed.")
        else:
            print(f"[ERROR] Startup Telegram test FAILED: {result}")
            print("Check your TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID env vars on Render.")
    except Exception as e:
        print(f"[ERROR] Cannot reach Telegram at all: {e}")

    # Start the monitor in a background thread
    monitor_thread = threading.Thread(target=run_monitor, daemon=True)
    monitor_thread.start()

    # Run Flask on the main thread (Render expects this)
    port = int(os.environ.get("PORT", 10000))
    print(f"[WEB] Starting Flask on port {port}")
    web_app.run(host="0.0.0.0", port=port)