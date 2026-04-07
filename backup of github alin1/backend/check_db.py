import chromadb
from pathlib import Path

DB_ROOT = Path("subject_dbs")
DB_MAP = {
    "rtl": DB_ROOT / "rtl_db",
    "python": DB_ROOT / "python_db",
    "maths": DB_ROOT / "maths_db",
    "english": DB_ROOT / "english_db"
}

def peek_inside():
    print("=== ALIN1 DATABASE HEALTH REPORT ===\n")
    for subject, path in DB_MAP.items():
        if not path.exists():
            print(f"❌ {subject.upper()}: Folder missing at {path}")
            continue
        
        try:
            client = chromadb.PersistentClient(path=str(path))
            collection = client.get_collection("book_content")
            count = collection.count()
            
            print(f"✅ {subject.upper()} DB: {count} text chunks found.")
            
            if count > 0:
                # Look at the very first chunk to check quality
                sample = collection.peek(1)
                text = sample['documents'][0]
                metadata = sample['metadatas'][0]
                print(f"   ﹂ Sample Text: {text[:100]}...")
                print(f"   ﹂ Metadata: {metadata}")
            else:
                print(f"   ⚠️ Warning: Collection exists but it is EMPTY.")
            print("-" * 40)
            
        except Exception as e:
            print(f"⚠️ {subject.upper()}: Error reading collection. (Did you index it yet?)")

if __name__ == "__main__":
    peek_inside()