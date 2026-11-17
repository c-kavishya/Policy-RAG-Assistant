from vector_store import client, collection, get_embeddings


def retrieve_chunks(question, top_k=4):
    query_embedding = get_embeddings([question], task_type="RETRIEVAL_QUERY")[0]

    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]

    retrieved = []
    for doc, meta, dist in zip(docs, metas, distances):
        retrieved.append({
            "text": doc,
            "source": meta["source"],
            "page": meta["page"],
            "distance": round(dist, 4),
        })
    return retrieved


def generate_answer(question, retrieved_chunks):
    context = "\n\n".join(
         [f"[Source: {c['source']}, Page {c['page']}]\n{c['text']}" for c in retrieved_chunks]
     )

    prompt = f"""You are a helpful company policy assistant.
Answer the question using ONLY the context provided below.
Cite the source filename and page number in your answer.
If the answer is not in the context, say "I don't know based on the provided policy documents."

Context:
{context}

Question: {question}
Answer:"""

    
    response = client.models.generate_content(model="gemini-3.8-flash", contents=prompt) 
    return response.text


if __name__ == "__main__":
    test_q = input("Ask a policy question: ")
    chunks = retrieve_chunks(test_q)

    print("\n--- Retrieved Chunks (Step 4 Check) ---")
    for c in chunks:
        print(f"- {c['source']} (Page {c['page']}, dist={c['distance']})")

    answer = generate_answer(test_q, chunks)
    print("\n--- Final Answer (Step 5 Check) ---")
    print(answer)