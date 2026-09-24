import requests
import html
import re
import xml.etree.ElementTree as ET


def get_posts(subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/new/.rss"

    headers = {
        "User-Agent": "CryptoRedditAlertBot/1.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

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

        # Reddit's RSS body contains HTML.
        body = html.unescape(body)

        # Remove HTML tags.
        body = re.sub(
            r"<[^>]+>",
            " ",
            body
        )

        # Clean extra whitespace.
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