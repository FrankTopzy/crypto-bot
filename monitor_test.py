from reddit_monitor import process_post


test_post = {
    "id": "TEST_FULL_PIPELINE_001",
    "title": "I can't withdraw my BTC from Coinbase",
    "body": "I have tried several times but my Bitcoin withdrawal is stuck.",
    "subreddit": "coinbase",
    "author": "test_user",
    "url": "https://www.reddit.com/r/coinbase/",
}

process_post(test_post)

print("\n✅ Full pipeline test completed.")