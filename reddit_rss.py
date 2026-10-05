import html
import re
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

import requests


LAST_REQUEST_TIME = 0

# Reduced from 65s to 3s - the RSS feed is public and handles faster polling.
# The old 65s delay caused a full cycle to take ~24 minutes across 22 subreddits.
REQUEST_DELAY = 3

# Only return posts made within the last 4 hours.
MAX_POST_AGE_HOURS = 4

HEADERS = {
    "User-Agent": "CryptoRedditAlertBot/1.0 by FrankTopzy"
}


def _parse_timestamp(text):
    """Parse an ISO 8601 timestamp string into a UTC datetime."""
    if not text:
        return None
    try:
        # Reddit uses format: 2024-01-15T12:34:56+00:00
        text = text.strip()
        # Replace Z suffix with +00:00 for compatibility
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        return datetime.fromisoformat(text)
    except (ValueError, TypeError):
        return None


def get_posts(subreddit):
    global LAST_REQUEST_TIME

    # Enforce minimum delay between Reddit requests.
    elapsed = time.time() - LAST_REQUEST_TIME

    if elapsed < REQUEST_DELAY:
        time.sleep(REQUEST_DELAY - elapsed)

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
            f"[WARNING] Reddit rate-limited r/{subreddit} (429). "
            f"Waiting {retry_seconds}s before continuing."
        )

        time.sleep(retry_seconds)
        return []

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

        # ── 4-hour recency filter ──────────────────────────────────────────
        post_time = _parse_timestamp(
            updated_element.text if updated_element is not None else None
        )

        if post_time is not None and post_time < cutoff:
            # Post is older than 4 hours — skip it.
            continue

        # ── Extract fields ─────────────────────────────────────────────────
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

        # Format post age for display
        age_str = ""
        if post_time is not None:
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
            "subreddit": subreddit,
            "author": author.replace("/u/", ""),
            "url": url,
            "age": age_str,
        })

    return posts