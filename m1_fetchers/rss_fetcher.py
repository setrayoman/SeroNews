# rss_fetcher.py

import feedparser
from datetime import datetime
from typing import List, Dict


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
        }
        articles.append(article)

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


# Example usage (you can comment this out when using as a module)
if __name__ == "__main__":
    test_url = "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"
    articles = fetch_articles(test_url)
    for i, article in enumerate(articles[:3], 1):
        print(f"{i}. {article['title']} ({article['published']})")
        print(f"   {article['link']}")
