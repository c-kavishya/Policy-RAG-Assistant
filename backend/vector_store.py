import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
import chromadb
from ingestion import extract_pages, chunk_pages


load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection(name="company_policies", metadata={"hnsw:space": "cosine"})


def get_embeddings(texts, task_type="RETRIEVAL_DOCUMENT"):
    response = client.models.embed_content(model="gemini-embedding-001", contents=texts, config=types.EmbedContentConfig(task_type=task_type))
    return [e.values for e in response.embeddings]


def store_chunks(chunks, batch_size=50):
    existing_ids = set(collection.get()["ids"])
    chunks = [c for c in chunks if c["chunk_id"] not in existing_ids]
    print(f"Remaining chunks to store: {len(chunks)}")

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]

        ids = [c["chunk_id"] for c in batch]
        texts = [c["text"] for c in batch]
        metadatas = [{"source": c["source"], "page": c["page"]} for c in batch]

        
        embeddings = get_embeddings(texts)
        collection.upsert(ids=ids, documents=texts, embeddings=embeddings, metadatas=metadatas)

        print(f"Stored batch {i // batch_size + 1} ({len(batch)} chunks)")
        time.sleep(35)  

if __name__ == "__main__":
    pages = extract_pages("data")
    chunks = chunk_pages(pages)
    print(f"Total chunks to store: {len(chunks)}")

    store_chunks(chunks)
    print("Total chunks in ChromaDB:", collection.count())