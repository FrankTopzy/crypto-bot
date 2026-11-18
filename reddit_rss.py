import html
import re
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

import requests


LAST_REQUEST_TIME = 0

# 5s between requests (up from 3s) — gives Reddit breathing room.
REQUEST_DELAY = 5

# Only return posts made within the last 5 hours.
MAX_POST_AGE_HOURS = 5

# Track consecutive 429s for exponential backoff.
_consecutive_429s = 0

HEADERS = {
    "User-Agent": "CryptoRedditAlertBot/1.0 by FrankTopzy"
}


def _parse_timestamp(text):
    """Parse an ISO 8601 timestamp string into a UTC datetime."""
    if not text:
        return None
    try:
        text = text.strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        return datetime.fromisoformat(text)
    except (ValueError, TypeError):
        return None


def get_posts(subreddit):
    """
    Fetch recent posts for one subreddit or a combined multi-sub string
    (e.g. "coinbase+kraken+metamask").

    When fetching a combined feed, each post's subreddit is extracted from
    the <category term="..."> element in the Atom entry.

    Returns a list of post dicts.
    """
    global LAST_REQUEST_TIME, _consecutive_429s

    # Enforce minimum delay between Reddit requests.
    elapsed = time.time() - LAST_REQUEST_TIME
    if elapsed < REQUEST_DELAY:
        time.sleep(REQUEST_DELAY - elapsed)

    url = f"https://www.reddit.com/r/{subreddit}/new/.rss?limit=50"

    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
    except requests.RequestException as e:
        print(f"[ERROR] Request failed for r/{subreddit}: {e}")
        LAST_REQUEST_TIME = time.time()
        return []

    LAST_REQUEST_TIME = time.time()

    # Handle Reddit rate limiting with exponential backoff.
    if response.status_code == 429:
        _consecutive_429s += 1

        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                base_wait = int(retry_after)
            except ValueError:
                base_wait = 60
        else:
            base_wait = 60

        # Exponential backoff: base * 2^(n-1), capped at 600s.
        wait_time = min(base_wait * (2 ** (_consecutive_429s - 1)), 600)

        print(
            f"[WARNING] Reddit rate-limited r/{subreddit} (429). "
            f"Backoff #{_consecutive_429s}, waiting {wait_time}s."
        )

        time.sleep(wait_time)
        return []

    # Reset backoff counter on any non-429 response.
    _consecutive_429s = 0

    # Skip private or restricted subreddits.
    if response.status_code == 403:
        print(
            f"[SKIP] r/{subreddit} is private or restricted (403)."
        )
        return []

    # Skip subreddits that don't exist.
    if response.status_code == 404:
        print(
            f"[SKIP] r/{subreddit} does not exist (404)."
        )
        return []

    response.raise_for_status()

    root = ET.fromstring(response.content)

    namespace = {
        "atom": "http://www.w3.org/2005/Atom"
    }

    now_utc = datetime.now(timezone.utc)
    cutoff = now_utc - timedelta(hours=MAX_POST_AGE_HOURS)

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

        updated_element = entry.find(
            "atom:updated",
            namespace
        )

        published_element = entry.find(
            "atom:published",
            namespace
        )

        category_element = entry.find(
            "atom:category",
            namespace
        )

        # ── 5-hour recency filter ──────────────────────────────────────────
        raw_date = ""
        if published_element is not None and published_element.text:
            raw_date = published_element.text
        elif updated_element is not None and updated_element.text:
            raw_date = updated_element.text

        post_time = _parse_timestamp(raw_date)

        if post_time is not None and post_time < cutoff:
            # Post is older than 5 hours — skip it.
            continue

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

        # Extract subreddit from <category> (works for multi-sub feeds).
        # Falls back to the subreddit string passed by the caller.
        post_subreddit = subreddit
        if category_element is not None:
            term = category_element.attrib.get("term", "")
            if term:
                post_subreddit = term

        entry_url = ""

        if link_element is not None:
            entry_url = link_element.attrib.get(
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

        # Format post age for display
        age_str = ""
        published_timestamp = None
        if post_time is not None:
            published_timestamp = post_time.timestamp()
            age_minutes = int(
                (now_utc - post_time).total_seconds() / 60
            )
            if age_minutes < 60:
                age_str = f"{age_minutes}m ago"
            else:
                age_str = f"{age_minutes // 60}h {age_minutes % 60}m ago"

        posts.append({
            "id": post_id,
            "title": title,
            "body": body,
            "subreddit": post_subreddit,
            "author": author.replace("/u/", ""),
            "url": entry_url,
            "age": age_str,
            "published_timestamp": published_timestamp,
        })

    return posts
