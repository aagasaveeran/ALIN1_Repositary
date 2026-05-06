import chromadb
from ollama import Client
from pathlib import Path
import os

# 1. Setup Clients
ollama_client = Client(host='http://127.0.0.1:11434')

# --- THE FIX: Use absolute path based on this file's location ---
current_dir = Path(__file__).parent.absolute()
db_path = current_dir / "subject_dbs" / "rtl_db"

print(f"Connecting to Database at: {db_path}")
client = chromadb.PersistentClient(path=str(db_path))

try:
    collection = client.get_collection(name="book_content")
    print(f"✅ Successfully connected. Total chunks in DB: {collection.count()}\n")
except Exception as e:
    print(f"❌ Could not load collection. Error: {e}")
    # Show what collections DO exist just in case
    print(f"Available collections in this DB: {client.list_collections()}")
    exit()

def get_chunk_id(search_term):
    print(f"🔍 Searching for: '{search_term}'")
    
    # 2. Create the math embedding for the search
    response = ollama_client.embeddings(
        model="nomic-embed-text:latest", 
        prompt=f"search_query: {search_term}"
    )
    
    # 3. Ask ChromaDB for the absolute best match
    results = collection.query(
        query_embeddings=[response['embedding']], 
        n_results=1, # We only want the top #1 perfect match
        include=["documents", "metadatas"]
    )
    
    if results['documents'] and results['documents'][0]:
        chunk_id = results['metadatas'][0][0].get('chunk_id', 'NO_ID_FOUND')
        preview = results['documents'][0][0].replace('\n', ' ')[:150] + "..."
        
        print(f"🎯 EXACT CHUNK ID : '{chunk_id}'")
        print(f"📝 Text Preview   : {preview}\n" + "-"*50 + "\n")
    else:
        print("❌ No matches found.\n")

# --- ENTER YOUR FAQ QUESTIONS HERE ---
get_chunk_id("What is CFSR?")
get_chunk_id("Define Integrity")
get_chunk_id("Who is the author of the syllabus?")