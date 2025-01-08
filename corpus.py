class Corpus:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.documents = {}
            cls._instance.authors = {}
            cls._instance.doc_count = 0
        return cls._instance

    def add_document(self, doc):
        self.doc_count += 1
        self.documents[self.doc_count] = doc
        
        if doc.author not in self.authors:
            self.authors[doc.author] = []
        self.authors[doc.author].append(doc)

    def get_stats(self):
        return {
            "total_docs": len(self.documents),
            "total_authors": len(self.authors),
            "docs_by_type": {
                "news": len([d for d in self.documents.values() if d.get_type() == "News"]),
                "wikipedia": len([d for d in self.documents.values() if d.get_type() == "Wikipedia"])
            }
        }
