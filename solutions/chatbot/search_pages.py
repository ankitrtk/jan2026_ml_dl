import os
import re
import json
import math
from collections import Counter

INDEX_DIR = "index"


class TextCleaner:
    def clean_and_tokenize(self, text):
        text = text.lower()
        text = re.sub(r"[^a-z0-9.%\s]", " ", text)
        text = re.sub(r"(?<!\d)\.(?!\d)", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text.split()


class IndexStore:
    def __init__(self, index_dir):
        self.index_dir = index_dir

    def load_json(self, filename):
        path = os.path.join(self.index_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_index(self):
        documents = self.load_json("documents.json")
        vocabulary = self.load_json("vocabulary.json")
        matrix = self.load_json("tfidf_matrix.json")
        idf_values = self.load_json("idf_values.json")
        return documents, vocabulary, matrix, idf_values


class Vectorizer:
    def __init__(self, vocabulary):
        self.vocabulary = vocabulary

    def vectorize(self, tokens):
        vector = [0] * len(self.vocabulary)
        counts = Counter(tokens)

        for word, count in counts.items():
            if word in self.vocabulary:
                index = self.vocabulary[word]
                vector[index] = count

        return vector

    def vectorize_tfidf_query(self, tokens, idf_values):
        word_count_vector = self.vectorize(tokens)
        total_words = sum(word_count_vector)

        tfidf_vector = []

        for word_index, count in enumerate(word_count_vector):
            if total_words == 0:
                tf = 0
            else:
                tf = count / total_words

            tfidf = tf * idf_values[word_index]
            tfidf_vector.append(tfidf)

        return tfidf_vector


class SimilaritySearch:
    def cosine_similarity(self, vector1, vector2):
        dot_product = 0
        norm1 = 0
        norm2 = 0

        for a, b in zip(vector1, vector2):
            dot_product += a * b
            norm1 += a * a
            norm2 += b * b

        if norm1 == 0 or norm2 == 0:
            return 0

        return dot_product / (math.sqrt(norm1) * math.sqrt(norm2))


class Retriever:
    def __init__(self, index_dir):
        store = IndexStore(index_dir)

        self.documents, self.vocabulary, self.matrix, self.idf_values = store.load_index()
        self.cleaner = TextCleaner()
        self.vectorizer = Vectorizer(self.vocabulary)
        self.similarity = SimilaritySearch()

    def search(self, query, top_k=2):
        query_tokens = self.cleaner.clean_and_tokenize(query)
        query_vector = self.vectorizer.vectorize_tfidf_query(
            query_tokens,
            self.idf_values
        )

        results = []

        for i, doc_vector in enumerate(self.matrix):
            score = self.similarity.cosine_similarity(query_vector, doc_vector)

            results.append({
                "page_name": self.documents[i]["page_name"],
                "score": score,
                "raw_text": self.documents[i]["raw_text"]
            })

        results.sort(key=lambda x: x["score"], reverse=True)

        return results[:top_k]


if __name__ == "__main__":
    retriever = Retriever(INDEX_DIR)

    while True:
        query = input("\nAsk question: ")

        if query.lower() in ["exit", "quit"]:
            break

        results = retriever.search(query, top_k=2)

        print("\nTop matching pages:")

        for result in results:
            print("----------------------------")
            print("Page:", result["page_name"])
            print("Score:", round(result["score"], 4))