from scraper import Scraper

def main():
    NEWS_API_KEY = "3a1cba260fa74b0c91d8b0aa9af197a4"  # Replace with your actual NewsAPI key

    scraper = Scraper(NEWS_API_KEY)
    
    # Scraping data
    scraper.scrape_news("pasta", 10)
    scraper.scrape_wikipedia("pasta", 10)
    
    # Output stats
    stats = scraper.corpus.get_stats()
    print("Corpus Statistics:")
    print(f"+----------------------+-------------------+")
    print(f"| Total Documents      | {stats['total_docs']}               |")
    print(f"| Total Authors        | {stats['total_authors']}             |")
    print(f"| News Articles        | {stats['docs_by_type']['news']}     |")
    print(f"| Wikipedia Articles   | {stats['docs_by_type']['wikipedia']} |")
    print(f"+----------------------+-------------------+\n")

    print("Documents in corpus:")
    print(f"+---------------------------------------------------+")
    print(f"| Title                                             |")
    print(f"+---------------------------------------------------+")
    for doc in scraper.corpus.documents.values():
        author = doc.author if doc.author else "Unknown"  # Handle None author
        print(f"| {doc.title:47} |")
        print(f"| Author: {author:35} |")
        print(f"| Date: {doc.date:37} |")
        print(f"| URL: {doc.url:45} |")
        print(f"| Type: {doc.get_type():42} |")
        
        print(f"| Full Text: {doc.text}... |")  # Show first 150 characters of the full text
        print(f"+---------------------------------------------------+")

if __name__ == "__main__":
    main()
