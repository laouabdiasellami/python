class Document:
    def __init__(self, title="", author="", date="", url="", text=""):
        self.title = title
        self.author = author
        self.date = date
        self.url = url
        self.text = text

    def __str__(self):
        return f"{self.title}, by {self.author}"

class NewsDocument(Document):
    def __init__(self, title="", author="", date="", url="", text="", source=""):
        super().__init__(title, author, date, url, text)
        self.source = source

    def __str__(self):
        return f"{super().__str__()} ({self.source})"

    def get_type(self):
        return "News"

class WikipediaDocument(Document):
    def __init__(self, title="", author="", date="", url="", text=""):
        super().__init__(title, author, date, url, text)

    def __str__(self):
        return f"{super().__str__()} (Wikipedia)"

    def get_type(self):
        return "Wikipedia"
