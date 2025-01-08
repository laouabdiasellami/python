from document import NewsDocument, WikipediaDocument

class DocumentFactory:
    @staticmethod
    def create_document(doc_type, **kwargs):
        if doc_type == "News":
            return NewsDocument(**kwargs)
        elif doc_type == "Wikipedia":
            return WikipediaDocument(**kwargs)
        raise ValueError(f"Unknown document type: {doc_type}")
