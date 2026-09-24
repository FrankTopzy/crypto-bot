import time

from filters import find_matches
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

    # Use your existing filter.
    matches = find_matches(
        title,
        body
    )

    # No relevant problem found.
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


def check_reddit():

    for subreddit in [
        "coinbase",
        "kraken",
        "trustwallet",
        "metamask",
        "tangem",
        "ledgerwallet",
        "phantom",
        "rabbywallet",
        "defi",
        "solana",
    ]:

        try:

            print(
                f"Checking r/{subreddit}..."
            )

            posts = get_posts(subreddit)

            for post in posts:
                process_post(post)

        except Exception as error:

            print(
                f"Error checking "
                f"r/{subreddit}: {error}"
            )


print("🚀 Crypto Reddit Alert Bot Started")


while True:

    check_reddit()

    print("Waiting 60 seconds...\n")

    time.sleep(60)