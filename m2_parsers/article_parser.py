from datetime import datetime
from m3_db import db

def parse_raw_articles():
    """
    Parse raw articles from 'articles' table and save them to 'parsed_articles'.
    """
    raw_articles = db.fetch_unparsed_articles()
    parsed_articles = []

    for raw in raw_articles:
        parsed_article = {
            "id": str(raw["id"]),
            "title": raw["title"],
            "url": raw["link"],
            "source": raw["source"],
            "author": None,
            "published_at": raw["published"],
            "fetched_at": datetime.utcnow().isoformat(),
            "content": raw["summary"] or "",
            "summary": raw["summary"] or "",
            "language": "en",
            "image_url": raw["image_url"],
            "tags": [],
            "related_stocks": [],
            "metadata": {
                "scraper_type": "rss",
                "original_html": None,
                "source_country": None,
                "source_language": "en"
            }
        }
        parsed_articles.append(parsed_article)

    # Save them using centralized DB handling
    db.save_parsed_articles(parsed_articles)

    # Mark articles as parsed
    article_ids = [raw["id"] for raw in raw_articles]
    db.mark_as_parsed(article_ids)

    print(f"✅ Saved {len(parsed_articles)} parsed articles to the database.")
