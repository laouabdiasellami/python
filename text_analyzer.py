from bs4 import BeautifulSoup
import re
import math
from collections import Counter, defaultdict

class TextAnalyzer:
    def __init__(self, corpus):
        self.corpus = corpus
        self.processed_docs = []
        self.vocabulary = set()
        self.doc_freqs = defaultdict(int)
        self.avg_doc_length = 0
        self.k1 = 1.5  # BM25 parameter
        self.b = 0.75  # BM25 parameter

    def clean_text(self, text):
        # Remove HTML tags using BeautifulSoup
        soup = BeautifulSoup(text, 'html.parser')
        text = soup.get_text()
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-z\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text

    def process_documents(self):
        # Process all documents
        for doc in self.corpus.documents.values():
            cleaned_text = self.clean_text(doc.text)
            tokens = cleaned_text.split()
            self.processed_docs.append({
                'tokens': tokens,
                'original_doc': doc
            })
            
            # Update vocabulary and document frequencies
            unique_terms = set(tokens)
            self.vocabulary.update(unique_terms)
            for term in unique_terms:
                self.doc_freqs[term] += 1

        # Calculate average document length for BM25
        total_length = sum(len(doc['tokens']) for doc in self.processed_docs)
        self.avg_doc_length = total_length / len(self.processed_docs) if self.processed_docs else 0

    def calculate_tfidf(self):
        N = len(self.processed_docs)
        tfidf_vectors = []

        for doc in self.processed_docs:
            term_freqs = Counter(doc['tokens'])
            vector = {}
            
            for term in self.vocabulary:
                tf = term_freqs[term]
                idf = math.log((N + 1) / (self.doc_freqs[term] + 1)) + 1
                vector[term] = tf * idf
            
            tfidf_vectors.append(vector)

        return tfidf_vectors

    def calculate_bm25_scores(self, query_tokens):
        N = len(self.processed_docs)
        scores = []

        for i, doc in enumerate(self.processed_docs):
            score = 0
            doc_length = len(doc['tokens'])
            term_freqs = Counter(doc['tokens'])

            for token in query_tokens:
                if token in self.vocabulary:
                    tf = term_freqs[token]
                    idf = math.log((N - self.doc_freqs[token] + 0.5) / 
                                 (self.doc_freqs[token] + 0.5) + 1)
                    
                    tf_scaled = ((tf * (self.k1 + 1)) / 
                               (tf + self.k1 * (1 - self.b + self.b * 
                                doc_length / self.avg_doc_length)))
                    
                    score += idf * tf_scaled

            scores.append((score, i))  # Store score and document index

        # Sort by scores and return the documents
        sorted_scores = sorted(scores, key=lambda x: x[0], reverse=True)
        return [(score, self.processed_docs[idx]['original_doc']) 
                for score, idx in sorted_scores]

    def cosine_similarity(self, vec1, vec2):
        dot_product = sum(vec1.get(term, 0) * vec2.get(term, 0) 
                         for term in self.vocabulary)
        
        mag1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
        mag2 = math.sqrt(sum(val ** 2 for val in vec2.values()))
        
        if mag1 == 0 or mag2 == 0:
            return 0
            
        return dot_product / (mag1 * mag2)

    def find_similar_documents(self, query_text, top_k=5):
        cleaned_query = self.clean_text(query_text)
        query_tokens = cleaned_query.split()
        
        query_tf = Counter(query_tokens)
        N = len(self.processed_docs)
        query_tfidf = {}
        
        for term in query_tf:
            tf = query_tf[term]
            idf = math.log((N + 1) / (self.doc_freqs[term] + 1)) + 1
            query_tfidf[term] = tf * idf

        doc_tfidf_vectors = self.calculate_tfidf()
        
        # Calculate cosine similarities
        cosine_scores = []
        for i, doc_vector in enumerate(doc_tfidf_vectors):
            similarity = self.cosine_similarity(query_tfidf, doc_vector)
            cosine_scores.append((similarity, i))
        
        # Sort by scores and get the documents
        sorted_cosine = sorted(cosine_scores, key=lambda x: x[0], reverse=True)
        cosine_results = [(score, self.processed_docs[idx]['original_doc']) 
                         for score, idx in sorted_cosine[:top_k]]
        
        # Get BM25 scores
        bm25_scores = self.calculate_bm25_scores(query_tokens)[:top_k]
        
        return {
            'cosine': cosine_results,
            'bm25': bm25_scores
        }