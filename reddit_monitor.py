from filters import find_matches
from telegram_bot import send_message


processed_posts = set()


def process_post(post):
    post_id = post["id"]

    # Check if we've already processed this post
    if post_id in processed_posts:
        print("Already processed. Skipping.")
        return

    # Remember this post
    processed_posts.add(post_id)

    title = post["title"]
    body = post["body"]

    matches = find_matches(title, body)

    if not matches:
        print("No match.")
        return

    for match in matches:
        message = (
            "🚨 CRYPTO ALERT\n\n"
            f"Type: {match}\n\n"
            f"📍 r/{post['subreddit']}\n\n"
            f"📝 {title}\n\n"
            f"👤 u/{post['author']}\n\n"
            f"🔗 {post['url']}"
        )

        print("🚨 MATCH FOUND")
        print(message)

        send_message(message)


# Fake Reddit post
fake_post = {
    "id": "abc123",
    "title": "I can't withdraw my BTC",
    "body": "My withdrawal has been pending for hours.",
    "subreddit": "coinbase",
    "author": "example_user",
    "url": "https://reddit.com/r/coinbase/example"
}


process_post(fake_post)
process_post(fake_post)