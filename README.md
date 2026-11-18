# Policy RAG Assistant

## Problem & Solution

Problem : Manually searching through long company policy PDFs (50–1000 pages) to find a specific rule takes significant time

Solution : This project builds a RAG system that answers user questions strictly from company policy PDFs, with source page citations.

## Tech Stack
- PDF Parsing : PyPDF
- Vector DB : ChromaDB
- LLM & Embeddings : Google Gemini API
- Backend : FastAPI
- Frontend : Streamlit

## Project Structure
- data/ : Include company policy pdfs
- backend/ : FastAPI + RAG logic
- frontend/ : Streamlit chat UI

## Setup & How to Run
1. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate

2. **Install dependencies:**
      pip install -r requirements.txt

3. **Set up environment variables:**
     Create a .env file in the root directory and add your Gemini API key:
             GEMINI_API_KEY=your_api_key_here

4. **Ingest and embed PDFs into ChromaDB (run once):**
     python backend/vector_store.py

5. **Start the FastAPI backend (Terminal 1):**
     uvicorn main:app --app-dir backend --reload

6. **Start the Streamlit frontend (Terminal 2):**
      streamlit run frontend/app.py                


