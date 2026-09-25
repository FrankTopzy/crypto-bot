import html
import re
import time
import xml.etree.ElementTree as ET

import requests


LAST_REQUEST_TIME = 0
REQUEST_DELAY = 65

HEADERS = {
    "User-Agent": "CryptoRedditAlertBot/1.0 by FrankTopzy"
}


def get_posts(subreddit):
    global LAST_REQUEST_TIME

    # Make sure there is enough time between Reddit requests.
    elapsed = time.time() - LAST_REQUEST_TIME

    if elapsed < REQUEST_DELAY:
        wait_time = REQUEST_DELAY - elapsed

        print(
            f"⏳ Waiting {wait_time:.0f}s before "
            f"checking r/{subreddit}..."
        )

        time.sleep(wait_time)

    url = f"https://www.reddit.com/r/{subreddit}/new/.rss"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=20
    )

    LAST_REQUEST_TIME = time.time()

    # Handle Reddit rate limiting.
    if response.status_code == 429:
        retry_after = response.headers.get("Retry-After")

        if retry_after:
            try:
                retry_seconds = int(retry_after)
            except ValueError:
                retry_seconds = 120
        else:
            retry_seconds = 120

        print(
            f"⚠️ Reddit rate-limited r/{subreddit} (429). "
            f"Waiting {retry_seconds}s before continuing."
        )

        time.sleep(retry_seconds)

        return []

    response.raise_for_status()

    root = ET.fromstring(response.content)

    namespace = {
        "atom": "http://www.w3.org/2005/Atom"
    }

    posts = []

    for entry in root.findall("atom:entry", namespace):

        title_element = entry.find(
            "atom:title",
            namespace
        )

        content_element = entry.find(
            "atom:content",
            namespace
        )

        id_element = entry.find(
            "atom:id",
            namespace
        )

        author_element = entry.find(
            "atom:author/atom:name",
            namespace
        )

        link_element = entry.find(
            "atom:link",
            namespace
        )

        title = (
            title_element.text
            if title_element is not None
            else ""
        )

        body = (
            content_element.text
            if content_element is not None
            else ""
        )

        post_id = (
            id_element.text
            if id_element is not None
            else ""
        )

        author = (
            author_element.text
            if author_element is not None
            else "unknown"
        )

        url = ""

        if link_element is not None:
            url = link_element.attrib.get(
                "href",
                ""
            )

        body = html.unescape(body)

        body = re.sub(
            r"<[^>]+>",
            " ",
            body
        )

        body = re.sub(
            r"\s+",
            " ",
            body
        ).strip()

        posts.append({
            "id": post_id,
            "title": title,
            "body": body,
            "subreddit": subreddit,
            "author": author.replace("/u/", ""),
            "url": url,
        })

    return posts