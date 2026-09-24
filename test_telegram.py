from telegram_bot import send_message

response = send_message(
    "🚨 TEST CRYPTO ALERT\n\n"
    "Type: Possible Scam\n\n"
    "📍 r/test\n\n"
    "📝 This is a test alert\n\n"
    "👤 u/test\n\n"
    "🔗 https://reddit.com"
)

print(response)