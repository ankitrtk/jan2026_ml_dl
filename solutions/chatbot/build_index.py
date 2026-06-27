import os
import re
import json
from collections import Counter
import math
import hashlib


INPUT_DIR = "icici_cc_pages"
INDEX_DIR = "index"

os.makedirs(INDEX_DIR, exist_ok=True)


class TextCleaner:
    def clean_and_tokenize(self, text):
        text = text.lower()

        # keep letters, numbers, %, decimal points
        text = re.sub(r"[^a-z0-9.%\s]", " ", text)

        # remove dots that are not decimal points
        text = re.sub(r"(?<!\d)\.(?!\d)", " ", text)

        text = re.sub(r"\s+", " ", text).strip()

        return text.split()


class DocumentLoader:
    def __init__(self, input_dir):
        self.input_dir = input_dir

    def calculate_hash(self, text):
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def load_documents(self):
        documents = []

        for filename in sorted(os.listdir(self.input_dir)):
            if not filename.endswith(".txt"):
                continue

            path = os.path.join(self.input_dir, filename)

            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

            documents.append({
                "doc_id": len(documents),
                "page_name": filename,
                "raw_text": text,
                "hash": self.calculate_hash(text)
            })

        return documents


class VocabularyBuilder:
    def build(self, documents):
        vocabulary = {}

        for doc in documents:
            for token in doc["tokens"]:
                if token not in vocabulary:
                    vocabulary[token] = len(vocabulary)

        return vocabulary


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


class IndexBuilder:
    def __init__(self, input_dir, index_dir):
        self.input_dir = input_dir
        self.index_dir = index_dir
        self.cleaner = TextCleaner()

    def load_old_documents(self):
        path = os.path.join(self.index_dir, "documents.json")

        if not os.path.exists(path):
            return {}

        with open(path, "r", encoding="utf-8") as f:
            old_documents = json.load(f)

        return {
            doc["page_name"]: doc
            for doc in old_documents
        }

    def build_index(self):
        loader = DocumentLoader(self.input_dir)
        documents = loader.load_documents()

        old_documents = self.load_old_documents()

        new_count = 0
        changed_count = 0
        unchanged_count = 0

        for doc in documents:
            old_doc = old_documents.get(doc["page_name"])

            if old_doc and old_doc.get("hash") == doc["hash"]:
                doc["tokens"] = old_doc["tokens"]
                unchanged_count += 1
            else:
                doc["tokens"] = self.cleaner.clean_and_tokenize(doc["raw_text"])

                if old_doc:
                    changed_count += 1
                else:
                    new_count += 1

        vocab_builder = VocabularyBuilder()
        vocabulary = vocab_builder.build(documents)

        vectorizer = Vectorizer(vocabulary)

        matrix = []
        for doc in documents:
            vector = vectorizer.vectorize(doc["tokens"])
            matrix.append(vector)

        # -------------------------
        # TF-IDF starts here
        # -------------------------

        tfidf_transformer = TfidfTransformer()

        idf_values = tfidf_transformer.calculate_idf(matrix)

        tfidf_matrix = tfidf_transformer.transform(
            matrix,
            idf_values
        )

        self.save_json("documents.json", documents)
        self.save_json("vocabulary.json", vocabulary)
        self.save_json("word_count_matrix.json", matrix)
        self.save_json("idf_values.json", idf_values)
        self.save_json("tfidf_matrix.json", tfidf_matrix)

        print("Index built successfully.")
        print(f"Documents: {len(documents)}")
        print(f"Vocabulary size: {len(vocabulary)}")
        print(f"New documents: {new_count}")
        print(f"Changed documents: {changed_count}")
        print(f"Unchanged documents: {unchanged_count}")

    def save_json(self, filename, data):
        path = os.path.join(self.index_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


class TfidfTransformer:
    def calculate_idf(self, word_count_matrix):
        total_documents = len(word_count_matrix)
        total_words = len(word_count_matrix[0])

        document_frequency = [0] * total_words

        for word_index in range(total_words):
            for doc_vector in word_count_matrix:
                if doc_vector[word_index] > 0:
                    document_frequency[word_index] += 1

        idf_values = []

        for df in document_frequency:
            idf = math.log((1 + total_documents) / (1 + df)) + 1
            idf_values.append(idf)

        return idf_values

    def transform(self, word_count_matrix, idf_values):
        tfidf_matrix = []

        for doc_vector in word_count_matrix:
            total_words_in_doc = sum(doc_vector)

            tfidf_vector = []

            for word_index, count in enumerate(doc_vector):
                if total_words_in_doc == 0:
                    tf = 0
                else:
                    tf = count / total_words_in_doc

                tfidf = tf * idf_values[word_index]
                tfidf_vector.append(tfidf)

            tfidf_matrix.append(tfidf_vector)

        return tfidf_matrix


if __name__ == "__main__":
    builder = IndexBuilder(INPUT_DIR, INDEX_DIR)
    builder.build_index()
