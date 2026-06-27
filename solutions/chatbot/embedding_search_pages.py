import os
import json
import math
from openai import OpenAI

INDEX_DIR = "chunk_embedding_index"
EMBEDDING_MODEL = "text-embedding-3-small"

OPENAI_API_KEY = open('/home/ankit/Documents/personal/cloudx/jan2026_ml_dl_ankit/jan2026_ml_dl/solutions/openapi-key').read().strip()
client = OpenAI(api_key=OPENAI_API_KEY)


class EmbeddingRetriever:
    def __init__(self, index_dir=INDEX_DIR):
        self.chunks = self.load_chunks(index_dir)

    def load_chunks(self, index_dir):
        path = os.path.join(index_dir, "chunks.json")

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_query_embedding(self, query):
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=query
        )

        return response.data[0].embedding, response.usage.total_tokens

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

    def search(self, query, top_k=5):
        query_embedding, tokens_used = self.get_query_embedding(query)

        results = []

        for chunk in self.chunks:
            score = self.cosine_similarity(
                query_embedding,
                chunk["embedding"]
            )

            results.append({
                "page_name": chunk["page_name"],
                "chunk_index": chunk["chunk_index"],
                "score": score,
                "chunk_text": chunk["chunk_text"]
            })

        results.sort(key=lambda x: x["score"], reverse=True)

        return results[:top_k], tokens_used


if __name__ == "__main__":
    retriever = EmbeddingRetriever()

    while True:
        query = input("\nAsk question: ")

        if query.lower() in ["exit", "quit"]:
            break

        results, tokens_used = retriever.search(query, top_k=5)

        print(f"\nEmbedding query tokens used: {tokens_used}")
        print("\nTop matching chunks:")

        for result in results:
            print("----------------------------")
            print("Page:", result["page_name"])
            print("Chunk:", result["chunk_index"])
            print("Score:", round(result["score"], 4))
            print(result["chunk_text"][:500])