import requests
from datetime import datetime
from document_factory import DocumentFactory
from corpus import Corpus

class Scraper:
    def __init__(self, news_api_key):
        self.corpus = Corpus()
        self.news_api_key = news_api_key

    def scrape_news(self, query, num_articles=1000):
        news_url = "https://newsapi.org/v2/everything"
        headers = {'X-Api-Key': self.news_api_key}
        params = {
            'q': query,
            'pageSize': num_articles,
            'language': 'en'
        }
        
        try:
            response = requests.get(news_url, headers=headers, params=params)
            articles = response.json().get('articles', [])[:num_articles]
            
            for article in articles:
                # Only add fields if they are not None or empty
                title = article.get('title', '').strip()
                author = article.get('author', '').strip() or 'Unknown'
                date = article.get('publishedAt', '').strip() or 'Unknown date'
                url = article.get('url', '').strip()
                text = article.get('description', '').strip()
                source = article.get('source', {}).get('name', '').strip()

                # Remove empty or unwanted text fields (e.g., '[Removed]')
                if text in [None, '[Removed]']:
                    text = None  # Exclude this field if it's '[Removed]' or None

                # Remove empty fields
                doc_fields = {
                    "title": title if title else None,
                    "author": author if author else None,
                    "date": date if date else None,
                    "url": url if url else None,
                    "text": text if text else None,
                    "source": source if source else None
                }

                # Create the document without empty fields
                doc = DocumentFactory.create_document(
                    "News", **{k: v for k, v in doc_fields.items() if v is not None}
                )
                self.corpus.add_document(doc)
                
        except Exception as e:
            print(f"Error scraping news: {e}")

    def scrape_wikipedia(self, query, num_articles=1000):
        try:
            wikipedia_url = f"https://en.wikipedia.org/w/api.php"
            params = {
                'action': 'query',
                'list': 'search',
                'srsearch': query,
                'format': 'json',
                'srlimit': num_articles
            }
            response = requests.get(wikipedia_url, params=params)
            results = response.json().get('query', {}).get('search', [])
            
            for result in results:
                # Only add fields if they are not None or empty
                title = result.get('title', '').strip()
                author = 'Wikipedia'  # Since we don't have a specific author
                date = str(datetime.now())  # Wikipedia pages don't have a publish date, so we use current time
                url = f"https://en.wikipedia.org/wiki/{result.get('title')}"
                text = result.get('snippet', '').strip()

                # Remove unwanted text (e.g., '[Removed]')
                if text in [None, '[Removed]']:
                    text = None  # Exclude this field if it's '[Removed]' or None

                # Remove empty fields
                doc_fields = {
                    "title": title if title else None,
                    "author": author if author else None,
                    "date": date if date else None,
                    "url": url if url else None,
                    "text": text if text else None
                }

                # Create the document without empty fields
                doc = DocumentFactory.create_document(
                    "Wikipedia", **{k: v for k, v in doc_fields.items() if v is not None}
                )
                self.corpus.add_document(doc)
                
        except Exception as e:
            print(f"Error scraping Wikipedia: {e}")
