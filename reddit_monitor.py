import json
import os
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from filters import SUBREDDITS, find_matches
from reddit_rss import get_posts
from telegram_bot import send_message


# Use a path relative to this file so it works on Railway Linux container and Windows alike.
PROCESSED_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "processed_posts.json"
)
MAX_POST_AGE_HOURS = 5
MAX_POST_AGE_SECONDS = MAX_POST_AGE_HOURS * 3600


def load_processed_posts():
    if not os.path.exists(PROCESSED_FILE):
        return set()

    try:
        with open(PROCESSED_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return set(data)

    except (json.JSONDecodeError, OSError):
        print("[WARNING] Could not load processed posts. Starting fresh.")
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
        print(f"[WARNING] Could not save processed posts: {error}")


processed_posts = load_processed_posts()


def process_post(post):
    post_id = post["id"]

    if post_id in processed_posts:
        return

    # Mark the post as processed immediately.
    processed_posts.add(post_id)
    save_processed_posts()

    # Only alert posts within the last 5 hours
    published_time = post.get("published_timestamp")
    if published_time:
        age_seconds = time.time() - published_time
        if age_seconds > MAX_POST_AGE_SECONDS:
            age_hours = age_seconds / 3600
            print(
                f"⏳ Skipping post older than {MAX_POST_AGE_HOURS}h "
                f"({age_hours:.1f}h old): {post['title']}"
            )
            return

    title = post["title"]
    body = post["body"]

    matches = find_matches(title, body)
    alert_type = " | ".join(matches) if matches else "New Post"
    age_label = f" ({post['age']})" if post.get("age") else ""

    message = (
        "🚨 REDDIT ALERT\n\n"
        f"🏷️ Type: {alert_type}\n\n"
        f"📍 r/{post['subreddit']}{age_label}\n\n"
        f"📝 {title}\n\n"
        f"👤 u/{post['author']}\n\n"
        f"🔗 {post['url']}"
    )

    print("\n🚨 ALERT SENT")
    print(message)

    send_message(message)


def seed_existing_posts():
    print(f"\n[SEED] Seeding existing Reddit posts (last {MAX_POST_AGE_HOURS} hours)...")
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

    print("\n[OK] Startup seeding complete.\n")


def check_reddit():
    for subreddit in SUBREDDITS:
        try:
            print(f"Checking r/{subreddit}...")

            posts = get_posts(subreddit)

            print(f"  Found {len(posts)} recent posts.")

            for post in posts:
                process_post(post)

        except Exception as error:
            print(
                f"Error checking r/{subreddit}: {error}"
            )


def start_monitor(interval=60):
    print("🚀 Crypto Reddit Alert Bot Started")
    print(f"📡 Monitoring {len(SUBREDDITS)} subreddits")
    print(f"⏱️ Checking every {interval} seconds")
    print(f"🕒 Alerting posts within the last {MAX_POST_AGE_HOURS} hours\n")

    if not processed_posts:
        seed_existing_posts()
    else:
        print(
            f"[OK] Loaded {len(processed_posts)} "
            "previously processed posts.\n"
        )

    while True:
        check_reddit()

        print(f"\nWaiting {interval} seconds...\n")
        time.sleep(interval)