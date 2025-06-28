from flask import Flask, render_template, request, redirect
import feedparser
import sqlite3
from m3_db import db

app = Flask(__name__)

def get_articles():
    conn = sqlite3.connect(db.DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM parsed_articles LIMIT 1")
    print(cursor.fetchone().keys())
    cursor.execute("SELECT * FROM parsed_articles ORDER BY published_at DESC LIMIT 20")
    articles = cursor.fetchall()
    conn.close()
    return articles

@app.route('/')
def index():
    articles = get_articles()
    return render_template('index_old.html', articles=articles)

# def home():
#     category = request.args.get('category', 'tech')
#     feed = feedparser.parse(RSS_FEEDS.get(category, RSS_FEEDS['tech']))
#     news_items = [{
#         'title': entry.title,
#         'link': entry.link,
#         'published': entry.published
#     } for entry in feed.entries[:10]]
#     return render_template('index_old.html', news=news_items, category=category)
#
# @app.route('/save', methods=['POST'])
# def save_article():
#     title = request.form['title']
#     link = request.form['link']
#     published = request.form['published']
#     with sqlite3.connect(DB) as conn:
#         c = conn.cursor()
#         c.execute("INSERT INTO saved_news (title, link, published) VALUES (?, ?, ?)",
#                   (title, link, published))
#         conn.commit()
#     return redirect('/saved')
#
# @app.route('/saved')
# def show_saved():
#     with sqlite3.connect(DB) as conn:
#         c = conn.cursor()
#         c.execute("SELECT id, title, link, published FROM saved_news")
#         articles = c.fetchall()
#     return render_template('saved.html', articles=articles)
#
# @app.route('/search')
# def search():
#     keyword = request.args.get('q', '')
#     with sqlite3.connect(DB) as conn:
#         c = conn.cursor()
#         c.execute("SELECT title, link, published FROM saved_news WHERE title LIKE ?", (f'%{keyword}%',))
#         results = c.fetchall()
#     return render_template('saved.html', articles=results, search=keyword)

if __name__ == '__main__':
    app.run(debug=True)
