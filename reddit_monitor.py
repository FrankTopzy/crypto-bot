import json
import os
import time

from filters import SUBREDDITS, find_matches
from reddit_rss import get_posts
from telegram_bot import send_message


PROCESSED_FILE = "/app/data/processed_posts.json"


def load_processed_posts():
    if not os.path.exists(PROCESSED_FILE):
        return set()

    try:
        with open(PROCESSED_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return set(data)

    except (json.JSONDecodeError, OSError):
        print("⚠️ Could not load processed posts. Starting fresh.")
        return set()


def save_processed_posts():
    try:
        with open(PROCESSED_FILE, "w", encoding="utf-8") as file:
            json.dump(
                list(processed_posts),
                file,
                indent=2
            )

    except OSError as error:
        print(f"⚠️ Could not save processed posts: {error}")


processed_posts = load_processed_posts()


def process_post(post):
    post_id = post["id"]

    if post_id in processed_posts:
        return

    # Mark the post as processed immediately.
    processed_posts.add(post_id)
    save_processed_posts()

    title = post["title"]
    body = post["body"]

    matches = find_matches(title, body)

    if not matches:
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

        print("\n🚨 MATCH FOUND")
        print(message)

        send_message(message)


def seed_existing_posts():
    print("\n🌱 Seeding existing Reddit posts...")
    print("Existing posts will NOT trigger Telegram alerts.\n")

    for subreddit in SUBREDDITS:
        try:
            print(f"Seeding r/{subreddit}...")

            posts = get_posts(subreddit)

            for post in posts:
                processed_posts.add(post["id"])

            save_processed_posts()

            print(
                f"Marked {len(posts)} existing posts as seen."
            )

        except Exception as error:
            print(
                f"Error seeding r/{subreddit}: {error}"
            )

    print("\n✅ Startup seeding complete.\n")


def check_reddit():
    for subreddit in SUBREDDITS:
        try:
            print(f"Checking r/{subreddit}...")

            posts = get_posts(subreddit)

            print(f"Found {len(posts)} posts.")

            for post in posts:
                process_post(post)

        except Exception as error:
            print(
                f"Error checking r/{subreddit}: {error}"
            )


def start_monitor(interval=60):
    print("🚀 Crypto Reddit Alert Bot Started")
    print(f"📡 Monitoring {len(SUBREDDITS)} subreddits")
    print(f"⏱️ Checking every {interval} seconds\n")

    if not processed_posts:
        seed_existing_posts()
    else:
        print(
            f"💾 Loaded {len(processed_posts)} "
            "previously processed posts.\n"
        )

    while True:
        check_reddit()

        print(f"\n⏳ Waiting {interval} seconds...\n")
        time.sleep(interval)