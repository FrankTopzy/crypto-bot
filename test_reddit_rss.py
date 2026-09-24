from reddit_rss import get_posts


posts = get_posts("coinbase")


print(f"Found {len(posts)} posts\n")


for post in posts[:5]:

    print("ID:", post["id"])
    print("Title:", post["title"])
    print("Author:", post["author"])
    print("URL:", post["url"])
    print("Body:", post["body"][:200])
    print("-" * 60)