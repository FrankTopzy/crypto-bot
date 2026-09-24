from filters import find_matches


tests = [
    {
        "title": "I was scammed on Coinbase",
        "body": "Someone convinced me to send my USDT to their wallet."
    },
    {
        "title": "I can't withdraw my BTC",
        "body": "My withdrawal has been pending for hours."
    },
    {
        "title": "I sent ETH to the wrong wallet",
        "body": "I accidentally transferred it to another address."
    },
    {
        "title": "Bitcoin price prediction",
        "body": "I think BTC will reach $150k this year."
    },
    {
        "title": "I was scammed buying a car",
        "body": "Someone took my money after I tried to buy a car."
    }
]


for test in tests:
    matches = find_matches(
        test["title"],
        test["body"]
    )

    print(f"\nTitle: {test['title']}")
    print(f"Matches: {matches}")