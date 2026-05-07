import chromadb
from ollama import Client
from pathlib import Path
import os

# 1. Setup Clients
ollama_client = Client(host='http://127.0.0.1:11434')
current_dir = Path(__file__).parent.absolute()
db_path = current_dir / "subject_dbs" / "rtl_db"

print(f"Connecting to Database at: {db_path}")
client = chromadb.PersistentClient(path=str(db_path))

# Use get_or_create to ensure we don't crash if it exists
collection = client.get_or_create_collection(name="book_content", metadata={"hnsw:space": "cosine"})

# 2. Read the book file
file_path = Path("/home/sama/Documents/GitHub/ALIN1_Repositary/backup of github alin1/backend/source_documents/rtl/rtl_full_book.txt")
if not file_path.exists():
    print(f"❌ Error: Could not find {file_path}")
    exit()

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 3. Split the text into chunks
# Your text is perfectly formatted with double newlines separating ideas!
raw_chunks = content.split("\n\n")
chunks = [c.strip() for c in raw_chunks if c.strip()]

print(f"📚 Found {len(chunks)} chunks to ingest. Starting embedding process...")

# 4. Embed and Save to ChromaDB
for i, chunk in enumerate(chunks):
    # Try to extract a nice topic from your [Context: ...] tags
    topic = "RTL Textbook"
    if chunk.startswith("[Context:"):
        first_line = chunk.split("]")[0] + "]"
        topic = first_line.replace("[Context:", "").strip()

    # Create the math embedding
    response = ollama_client.embeddings(
        model="nomic-embed-text:latest", 
        prompt=f"search_document: {chunk}"
    )
    
    # Create a unique ID for this chunk
    chunk_id = f"BookSection_{i+1}"
    
    # Upsert (Update or Insert) into the database
    collection.upsert(
        ids=[chunk_id],
        embeddings=[response['embedding']],
        documents=[chunk],
        metadatas=[{"chunk_id": chunk_id, "topic": topic}]
    )
    
    print(f"✅ Embedded {i+1}/{len(chunks)}: {chunk_id}")

print("\n🎉 SUCCESS! The entire RTL book is now permanently stored in ChromaDB.")