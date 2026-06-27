import os
import json
import hashlib
from openai import OpenAI

INPUT_DIR = "icici_cc_pages"
INDEX_DIR = "chunk_embedding_index"
EMBEDDING_MODEL = "text-embedding-3-small"

CHUNK_SIZE = 500      # words
CHUNK_OVERLAP = 75   # words

OPENAI_API_KEY = open('/home/ankit/Documents/personal/cloudx/jan2026_ml_dl_ankit/jan2026_ml_dl/solutions/openapi-key').read().strip()
client = OpenAI(api_key=OPENAI_API_KEY)
os.makedirs(INDEX_DIR, exist_ok=True)


def calculate_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def split_into_chunks(text, chunk_size=500, overlap=75):
    words = text.split()
    chunks = []

    start = 0
    chunk_index = 0

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)

        if chunk_text.strip():
            chunks.append({
                "chunk_index": chunk_index,
                "chunk_text": chunk_text
            })

        chunk_index += 1
        start = end - overlap

    return chunks


def load_old_chunks():
    path = os.path.join(INDEX_DIR, "chunks.json")

    if not os.path.exists(path):
        return {}

    with open(path, "r", encoding="utf-8") as f:
        old_chunks = json.load(f)

    return {
        chunk["chunk_id"]: chunk
        for chunk in old_chunks
    }


def get_embedding(text):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.data[0].embedding, response.usage.total_tokens


def build_index():
    old_chunks = load_old_chunks()
    all_chunks = []

    new_count = 0
    reused_count = 0
    total_embedding_tokens = 0

    for filename in sorted(os.listdir(INPUT_DIR)):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(INPUT_DIR, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            raw_text = f.read()

        page_hash = calculate_hash(raw_text)
        chunks = split_into_chunks(raw_text, CHUNK_SIZE, CHUNK_OVERLAP)

        for chunk in chunks:
            chunk_id = f"{filename}_{chunk['chunk_index']}_{page_hash}"

            old_chunk = old_chunks.get(chunk_id)

            if old_chunk:
                all_chunks.append(old_chunk)
                reused_count += 1
                continue

            embedding, tokens_used = get_embedding(chunk["chunk_text"])
            total_embedding_tokens += tokens_used

            all_chunks.append({
                "chunk_id": chunk_id,
                "page_name": filename,
                "page_hash": page_hash,
                "chunk_index": chunk["chunk_index"],
                "chunk_text": chunk["chunk_text"],
                "embedding": embedding
            })

            new_count += 1
            print(f"Embedded: {chunk_id}")

    output_path = os.path.join(INDEX_DIR, "chunks.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False)

    print("\nChunk embedding index built.")
    print(f"Total chunks: {len(all_chunks)}")
    print(f"New chunks embedded: {new_count}")
    print(f"Reused chunks: {reused_count}")
    print(f"Embedding tokens used this run: {total_embedding_tokens}")


if __name__ == "__main__":
    build_index()