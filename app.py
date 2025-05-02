from flask import Flask, render_template, request, redirect
import feedparser
import sqlite3

app = Flask(__name__)
DB = 'news.db'

# RSS feeds per category
RSS_FEEDS = {
    'tech': 'https://www.theverge.com/rss/index.xml',
    'science': 'https://rss.sciam.com/sciam/technology',
    'world': 'https://rss.nytimes.com/services/xml/rss/nyt/World.xml'
}

# Create database and table
def init_db():
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS saved_news (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        link TEXT,
                        published TEXT
                    )''')
        conn.commit()

@app.route('/')
def home():
    category = request.args.get('category', 'tech')
    feed = feedparser.parse(RSS_FEEDS.get(category, RSS_FEEDS['tech']))
    news_items = [{
        'title': entry.title,
        'link': entry.link,
        'published': entry.published
    } for entry in feed.entries[:10]]
    return render_template('index.html', news=news_items, category=category)

@app.route('/save', methods=['POST'])
def save_article():
    title = request.form['title']
    link = request.form['link']
    published = request.form['published']
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO saved_news (title, link, published) VALUES (?, ?, ?)",
                  (title, link, published))
        conn.commit()
    return redirect('/saved')

@app.route('/saved')
def show_saved():
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute("SELECT id, title, link, published FROM saved_news")
        articles = c.fetchall()
    return render_template('saved.html', articles=articles)

@app.route('/search')
def search():
    keyword = request.args.get('q', '')
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute("SELECT title, link, published FROM saved_news WHERE title LIKE ?", (f'%{keyword}%',))
        results = c.fetchall()
    return render_template('saved.html', articles=results, search=keyword)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
