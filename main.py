from reddit_monitor import process_post, start_monitor


test_post = {
    "id": "RAILWAY_FULL_PIPELINE_TEST_001",
    "title": "I can't withdraw my BTC from Coinbase",
    "body": "I have tried several times but my Bitcoin withdrawal is stuck.",
    "subreddit": "coinbase",
    "author": "railway_test_user",
    "url": "https://www.reddit.com/r/coinbase/",
}


if __name__ == "__main__":
    process_post(test_post)

    start_monitor()