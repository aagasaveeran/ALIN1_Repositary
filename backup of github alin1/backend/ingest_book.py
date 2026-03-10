import chromadb
from pathlib import Path
import uuid
from rag_core import embed_text, DB_MAP

def ingest_document(file_path: str, subject: str, chunk_size=1000, overlap=200):
    path = Path(file_path)
    if not path.exists():
        print(f"❌ File not found: {file_path}")
        return

    print(f"📖 Reading {path.name} for {subject.upper()}...")
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. SMART CHUNKING
    # We create overlapping chunks so facts aren't cut in half
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i : i + chunk_size])

    print(f"🧩 Split into {len(chunks)} chunks. Starting embedding...")

    # 2. CONNECT TO CHROMA
    client = chromadb.PersistentClient(path=str(DB_MAP[subject]))
    collection = client.get_or_create_collection(
        name="book_content", 
        metadata={"hnsw:space": "cosine"}
    )

    # 3. UPSERT DATA
    for i, chunk in enumerate(chunks):
        chunk_id = f"Section {i}"
        # We use the embed_text function from your rag_core
        vector = embed_text(chunk, task_type="document")
        
        collection.add(
            ids=[str(uuid.uuid4())],
            embeddings=[vector],
            metadatas=[{"chunk_id": chunk_id, "subject": subject, "source": path.name}],
            documents=[chunk]
        )
        if i % 10 == 0:
            print(f"✅ Indexed {i}/{len(chunks)} chunks...")

    print(f"🎉 Successfully taught ALIN1 the {subject.upper()} material!")

if __name__ == "__main__":
    # --- CHANGE THESE TO YOUR ACTUAL FILE PATHS ---
    # Example:
    # ingest_document("my_maths_book.txt", "maths")
    # ingest_document("grammar_notes.txt", "english")
    
    file_to_load = input("Enter path to text file: ")
    subject_to_load = input("Enter subject (rtl/python/maths/english): ").lower()
    
    ingest_document(file_to_load, subject_to_load)