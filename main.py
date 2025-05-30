from m1_fetchers import rss_fetcher
from m2_parsers.article_parser import parse_raw_articles
from m3_db import db

def main():
    db.init_db()

    rss_feeds = [
        "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
        "https://feeds.bbci.co.uk/news/technology/rss.xml",
    ]

    all_articles = []

    for url in rss_feeds:
        print(f"Fetching from: {url}")
        articles = rss_fetcher.fetch_articles(url)
        all_articles.extend(articles)
    # Optionally: process articles
    for article in all_articles:
        # You can add NLP classification here if needed
        # article['category'] = classifier.classify_article(article['summary'])
        print(f"- {article['title']} ({article['published']}) [{article['source']}]")

    db.save_articles(all_articles)
    print(f"✅ Saved {len(all_articles)} articles.")

    # ✨ Parse raw articles to unified format
    parse_raw_articles()
    print("✅ Parsing of raw articles completed and inserted into parsed_articles.")

if __name__ == "__main__":
    main()
