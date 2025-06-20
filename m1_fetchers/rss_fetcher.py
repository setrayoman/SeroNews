# rss_fetcher.py

import feedparser
from datetime import datetime
from typing import List, Dict
from bs4 import BeautifulSoup
import json
import os

def fetch_articles(feed_url: str) -> List[Dict]:
    """
    Fetch articles from an RSS feed URL.

    Args:
        feed_url (str): The URL of the RSS feed.

    Returns:
        List[Dict]: A list of articles in standardized dictionary format.
    """
    feed = feedparser.parse(feed_url)
    articles = []

    for entry in feed.entries:
        article = {
            "title": entry.get("title", "No Title"),
            "link": entry.get("link", ""),
            "summary": entry.get("summary", ""),
            "published": parse_date(entry),
            "source": feed.feed.get("title", "Unknown Source"),
            "image_url": get_image_url(entry),
        }
        articles.append(article)
        print(article["image_url"])

    return articles


def parse_date(entry) -> str:
    for attr in ('published_parsed', 'updated_parsed'):
        parsed = getattr(entry, attr, None)
        if parsed:
            try:
                dt = datetime(*parsed[:6])
                return dt.isoformat()
            except Exception:
                continue
    return ""

def get_image_url(entry) -> str:

    image_url = None
    if 'media_content' in entry:
        media = entry['media_content'][0]
        image_url = media.get('url', "")
        print(f" fetch image url from media_content")
    elif 'media_thumbnail' in entry:
        image_url = entry['media_thumbnail'][0]['url']
        print(f" fetch image url from media_thumbnail")
    else:
        # try parsing summary for <img>
        if 'summary' in entry:
            soup = BeautifulSoup(entry.summary, 'html.parser')
            img = soup.find('img')
            if img and 'src' in img.attrs:
                image_url = img['src']
                print(f" fetch image url from <img>")
    return image_url or ""