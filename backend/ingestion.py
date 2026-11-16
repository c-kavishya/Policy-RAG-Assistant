import os
from pypdf import PdfReader

def extract_pages(data_dir):
    pages = []

    for filename in os.listdir(data_dir):
        if filename.endswith(".pdf"):
            file_path = os.path.join(data_dir,filename)
            reader = PdfReader(file_path)

            for page_num, page in enumerate(reader.pages, start = 1):
                text = page.extract_text() or ""

                text = " ".join(text.split())

                if text:
                    pages.append({"text": text,"source": filename,"page": page_num})

    return pages


def chunk_pages(pages, chunk_size=800, overlap=150):
    chunks = []

    for page_data in pages:
        text = page_data["text"]
        source = page_data["source"]
        page = page_data["page"]

        start = 0
        chunk_index = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))

            if end < len(text):
                space_idx = text.rfind(" ", start, end)
                if space_idx > start:
                    end = space_idx

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunk_id = f"{source}_p{page}_c{chunk_index}"
                chunks.append({"chunk_id": chunk_id, "text": chunk_text, "source": source, "page": page})
                chunk_index += 1

            
            if end == len(text):
                break
            start = end - overlap

    return chunks

if __name__ == "__main__":
    pages = extract_pages("data")
    print("Total pages extracted:", len(pages))
    if pages:
        print("First page:", pages[0]["source"], "Page:", pages[0]["page"])

    chunks = chunk_pages(pages)
    print("Total chunks created:", len(chunks))
    if len(chunks) >= 2:
        print("\nChunk 0:", chunks[0])
        print("\nChunk 1:", chunks[1])     