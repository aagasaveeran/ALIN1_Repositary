import os
import sys
import chromadb
# We import the embedding function, but we handle the loop here
from rag_core import embed_text, BOOK_DB_PATH

print("🚀 SCRIPT STARTED: Safe Ingestion Mode")

# 1. Setup Client
client = chromadb.PersistentClient(path=str(BOOK_DB_PATH))

# 2. Reset the collection to start fresh
try:
    client.delete_collection("book_content")
    print("   - Old database cleared.")
except:
    pass

# NEW (Forces Cosine Distance)
collection = client.create_collection(
    name="book_content", 
    metadata={"hnsw:space": "cosine"} # 👈 This is the magic key
)

def smart_chunk_text(text, max_chars=1000):
    """
    Splits text into chunks that are safe for the embedding model.
    1. Splits by paragraphs (double newline).
    2. If a paragraph is still too big, splits it by sentences/words.
    """
    raw_paragraphs = text.split('\n\n')
    safe_chunks = []
    
    for para in raw_paragraphs:
        para = para.strip()
        if not para:
            continue
            
        # If paragraph is safe size, add it
        if len(para) < max_chars:
            safe_chunks.append(para)
        else:
            # If paragraph is HUGE, slice it up by words
            words = para.split(' ')
            current_chunk = ""
            
            for word in words:
                # Check if adding the next word exceeds the limit
                if len(current_chunk) + len(word) + 1 < max_chars:
                    current_chunk += " " + word
                else:
                    safe_chunks.append(current_chunk.strip())
                    current_chunk = word
            
            # Add the leftover piece
            if current_chunk:
                safe_chunks.append(current_chunk.strip())
                
    return safe_chunks

def ingest_text_file(file_path):
    print(f"📖 Reading: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"❌ ERROR: Could not find file '{file_path}'")
        return

    # Use the new Smart Chunker
    print("🔪 Slicing text into safe chunks...")
    chunks = smart_chunk_text(text)
    
    if not chunks:
        print("❌ ERROR: File ended up empty after processing!")
        return

    print(f"🔍 Found {len(chunks)} safe chunks. Generating embeddings...")
    
    # Process in batches to show progress
    total = len(chunks)
    batch_size = 10
    
    for i in range(0, total, batch_size):
        batch = chunks[i : i + batch_size]
        
        # Create IDs and Metadata for this batch
        ids = [f"chunk_{i+j}" for j in range(len(batch))]
        metadatas = [{"chunk_id": f"Section {i+j}", "source": file_path} for j in range(len(batch))]
        
        # Embed and Add
        try:
            # We explicitly use task_type="document" for storage
            embeddings = [embed_text(c, task_type="document") for c in batch]
            
            collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=batch,
                metadatas=metadatas
            )
            print(f"   - Processed {i + len(batch)}/{total} chunks...", end='\r')
        except Exception as e:
            print(f"\n❌ Error on batch starting at index {i}: {e}")
            # Skip this batch and continue
            continue
            
    print(f"\n✅ SUCCESS: Ingestion complete! Database is ready.")

if __name__ == "__main__":
    # Point this to your actual file name
    target_file = "rtl-Copy.txt" 
    ingest_text_file(target_file)