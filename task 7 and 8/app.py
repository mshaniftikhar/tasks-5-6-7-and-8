from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)
API_KEY = "900b473053ca4dd6ab4fa228afa0a050"  

def get_news():
    articles = []
    try:
        url1 = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"
        response1 = requests.get(url1)
        response1.raise_for_status()  
        data1 = response1.json().get("articles", [])
        articles.extend(data1)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from NewsAPI: {e}")

    return articles

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    articles = get_news()
    filtered_articles = [article for article in articles if query and query.lower() in article.get('title', '').lower()]
    return render_template('index.html', articles=filtered_articles)

@app.route('/')
def home():
    articles = get_news()
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)