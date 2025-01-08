from scraper import Scraper
from text_analyzer import TextAnalyzer

def display_results(results):
    print("\nTop Results by Cosine Similarity:")
    print("-" * 80)
    for score, doc in results['cosine']:
        print(f"Score: {score:.4f}")
        print(f"Title: {doc.title}")
        print(f"Author: {doc.author}")
        print(f"Type: {doc.get_type()}")
        print(f"URL: {doc.url}")
        print("-" * 80)

    print("\nTop Results by BM25 Similarity:")
    print("-" * 80)
    for score, doc in results['bm25']:
        print(f"Score: {score:.4f}")
        print(f"Title: {doc.title}")
        print(f"Author: {doc.author}")
        print(f"Type: {doc.get_type()}")
        print(f"URL: {doc.url}")
        print("-" * 80)

def main():
    NEWS_API_KEY = "3a1cba260fa74b0c91d8b0aa9af197a4"  # Replace with your actual NewsAPI key

    # Initialize scraper
    scraper = Scraper(NEWS_API_KEY)
    
    # Enter your search topic
    search_topic = input("Enter topic to search (e.g., 'covid', 'climate change'): ")
    
    # Number of articles to fetch
    num_articles = 10  # You can change this number
    
    print(f"\nFetching {num_articles} articles about '{search_topic}'...")
    
    # Scraping data
    scraper.scrape_news(search_topic, num_articles)
    scraper.scrape_wikipedia(search_topic, num_articles)
    
    # Initialize text analyzer
    print("\nProcessing and analyzing texts...")
    analyzer = TextAnalyzer(scraper.corpus)
    analyzer.process_documents()
    
    # Output stats
    stats = scraper.corpus.get_stats()
    print("\nCorpus Statistics:")
    print(f"+----------------------+-------------------+")
    print(f"| Total Documents      | {stats['total_docs']}               |")
    print(f"| Total Authors        | {stats['total_authors']}             |")
    print(f"| News Articles        | {stats['docs_by_type']['news']}     |")
    print(f"| Wikipedia Articles   | {stats['docs_by_type']['wikipedia']} |")
    print(f"+----------------------+-------------------+\n")

    # Search functionality
    while True:
        query = input("\nEnter your search query (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
            
        results = analyzer.find_similar_documents(query, top_k=5)
        display_results(results)

if __name__ == "__main__":
    main()