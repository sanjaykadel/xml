from flask import Flask, render_template
import feedparser
import html

app = Flask(__name__)


def parse(rss_feed_url):
    try:
        feed = feedparser.parse(rss_feed_url)

        # Verify feed status
        if feed.status != 200:
            raise Exception("Failed to fetch RSS feed")

        # Extract necessary data from the feed
        items = []
        for entry in feed.entries:
            item = {
                'title': entry.title,
                'link': entry.link,
                'description': entry.get('description', ''),
                'pubDate': entry.get('published', ''),
                'author': entry.get('author', ''),
                'categories': [category.term for category in entry.get('tags', [])],
            }
            content = html.unescape(entry.get('content', [])[0].value if entry.get('content') else '')
            if content:
                item['content'] = content
            items.append(item)

        return render_template('index.html', items=items)
    except Exception as e:
        return "Error: " + str(e)


@app.route('/arthasarokar')
def index():
    url = 'https://arthasarokar.com/category/share-market/feed'
    data = parse(url)
    return data

@app.route('/arthasansar')
def home():
    url = 'https://arthasansar.com/feeds'
    data = parse(url)
    return data



if __name__ == '__main__':
    app.run(debug=True)
