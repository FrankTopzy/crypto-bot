import time

from filters import SUBREDDITS, find_matches
from reddit_rss import get_posts
from telegram_bot import send_message


processed_posts = set()


def process_post(post):
    post_id = post["id"]

    # Don't process the same Reddit post twice.
    if post_id in processed_posts:
        return

    processed_posts.add(post_id)

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

        response = send_message(message)
        print("Telegram response:", response)


def check_reddit():
    for subreddit in SUBREDDITS:
        try:
            print(f"Checking r/{subreddit}...")

            posts = get_posts(subreddit)

            print(
                f"Found {len(posts)} posts."
            )

            for post in posts:
                process_post(post)

        except Exception as error:
            print(
                f"Error checking "
                f"r/{subreddit}: {error}"
            )


def start_monitor(interval=60):
    print("🚀 Crypto Reddit Alert Bot Started")
    print(
        f"📡 Monitoring "
        f"{len(SUBREDDITS)} subreddits"
    )
    print(
        f"⏱️ Checking every "
        f"{interval} seconds\n"
    )

    while True:
        check_reddit()

        print(
            f"\n⏳ Waiting "
            f"{interval} seconds...\n"
        )

        time.sleep(interval)