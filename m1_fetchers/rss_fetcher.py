# rss_fetcher.py

import feedparser
from datetime import datetime
from typing import List, Dict
from bs4 import BeautifulSoup
import json
import os

JSON_FILE = 'financial_articles.json'


# RSS feeds per category
RSS_FEEDS = {
    'investing_economy': 'https://www.investing.com/rss/news_14.rss',
    'investing_stocks': 'https://www.investing.com/rss/news_25.rss',
    'cnn_ekonomi': 'https://www.cnnindonesia.com/ekonomi/rss',
    'cnbc_indonesia': 'https://www.cnbcindonesia.com/market/rss/'
}

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


def rss_test():
    # load existing articles if file exists
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            saved_articles = json.load(f)

    else:
        saved_articles = []

    # convert to a set of links for easy duplicate checking
    existing_links = {article['link'] for article in saved_articles}


    new_articles = []

    for name,url in RSS_FEEDS.items():
        print(f"\n--- Feed: {url} ---")
        print(f"--- Name: {name} ---")
        feed = feedparser.parse(url)

        if 'title' in feed.feed:
            print(f"feed Title: {feed.feed.title}")

        for entry in feed.entries[:3]:
            link = entry.link

            # skip duplicates
            if link in existing_links:
                continue

            # Try to get image
            image_url = None
            if 'media_content' in entry:
                image_url = entry
                print(f" fetch image url from media_content")
            elif 'media_thumbnail' in entry:
                image_url = entry
                print(f" fetch image url from media_thumbnail")
            else:
                # try parsing summary for <img>
                if 'summary' in entry:
                    soup = BeautifulSoup(entry.summary, 'html.parser')
                    img = soup.find('img')
                    if img and 'src' in img.attrs:
                        image_url = img['src']
                        print(f" fetch image url from <img>")

            print(f"• {entry.title}")
            print(f"  Link: {entry.link}")
            print(f"  Published: {entry.published if 'published' in entry else 'N/A'}")
            print(f"  image: {image_url}\n")

            article = {
                'source': feed.feed.title if 'title' in feed.feed else url,
                'title': entry.title,
                'link': link,
                'publised': entry.published if 'published' in entry else 'N/A',
                'image': image_url,
                'fetch_at': datetime.now().isoformat() #optional metadata
            }
            new_articles.append(article)
            existing_links.add(link) #update set

    # merge as save
    if new_articles:
        saved_articles.extend(new_articles)
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(saved_articles, f, ensure_ascii=False, indent=2)
        print(f"✅ {len(new_articles)} new articles saved.")
    else:
        print("🔁 No new articles found.")



# Example usage (you can comment this out when using as a module)
if __name__ == "__main__":
    test_url = "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"
    articles = fetch_articles(test_url)
    for i, article in enumerate(articles[:3], 1):
        print(f"{i}. {article['title']} ({article['published']})")
        print(f"   {article['link']}")