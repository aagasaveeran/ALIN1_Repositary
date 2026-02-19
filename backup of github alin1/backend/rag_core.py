# import chromadb
# from pathlib import Path
# import ollama
# import sys
# import os

# MODEL_NAME = "llama3:latest"
# EMBEDDING_MODEL = "nomic-embed-text:latest"

# # TWO DATABASES
# CHROMA_CHAT_PATH = Path("chroma_memory_db")
# BOOK_DB_PATH = Path("book_rag_db")

# # Chat memory collection
# chat_client = chromadb.PersistentClient(path=str(CHROMA_CHAT_PATH))

# # Book RAG collection
# book_client = chromadb.PersistentClient(path=str(BOOK_DB_PATH))
# try:
#     book_collection = book_client.get_collection("book_content")
# except:
#     book_collection = None

# MAX_CONTEXT_TURNS = 3
# MAX_BOOK_CHUNKS = 4

# def embed_text(text: str):
#     response = ollama.embeddings(model=EMBEDDING_MODEL, prompt=text)
#     return response['embedding']

# def get_or_create_chat_collection():
#     """Get or create chat collection, handling dimension mismatches."""
#     try:
#         collection = chat_client.get_collection(name="chat_memory")
#         if collection.count() > 0:
#             test_embedding = embed_text("test")
#             try:
#                 collection.query(query_embeddings=[test_embedding], n_results=1)
#             except Exception as e:
#                 if "dimension" in str(e).lower():
#                     print("⚠️ Chat collection has incompatible embedding dimension. Recreating...")
#                     chat_client.delete_collection(name="chat_memory")
#                     collection = chat_client.create_collection(
#                         name="chat_memory", metadata={"hnsw:space": "cosine"})
#         return collection
#     except:
#         return chat_client.create_collection(
#             name="chat_memory", metadata={"hnsw:space": "cosine"})

# chat_collection = get_or_create_chat_collection()

# def add_memory(user_text: str, assistant_text: str):
#     combined_text = f"User: {user_text}\nAssistant: {assistant_text}"
#     try:
#         next_id = len(chat_collection.get().get("ids", [])) + 1
#         chat_collection.add(
#             embeddings=[embed_text(combined_text)],
#             documents=[combined_text],
#             metadatas=[{"type": "conversation_turn"}],
#             ids=[f"turn_{next_id}"]
#         )
#     except Exception as e:
#         if "dimension" in str(e).lower():
#             print("⚠️ Embedding dimension mismatch in memory storage. Skipping save.")
#         else:
#             raise

# def clear_chat_history(confirm_text=None):
#     """🗑️ Clear ALL chat history. For API: pass confirm_text='YES'"""
#     if confirm_text == 'YES':
#         all_data = chat_collection.get()
#         ids = all_data.get("ids", [])
#         if ids:
#             chat_collection.delete(ids=ids)
#         return f"✅ Cleared {len(ids)} chat turns!"
#     return "ℹ️ No chat history to clear."

# def retrieve_book_rag(query: str, n_results=MAX_BOOK_CHUNKS):
#     """RAG: Search your 12k-line book."""
#     if not book_collection or book_collection.count() == 0:
#         return []
#     try:
#         query_embedding = embed_text(query)
#         results = book_collection.query(
#             query_embeddings=[query_embedding],
#             n_results=n_results,
#             include=["documents", "distances"]
#         )
#         relevant_chunks = []
#         if results['documents'] and results['distances']:
#             for doc, dist in zip(results['documents'][0], results['distances'][0]):
#                 if dist < 0.7:
#                     relevant_chunks.append(doc)
#         return relevant_chunks
#     except Exception as e:
#         if "dimension" in str(e).lower():
#             print(f"\n⚠️ ERROR: Book collection has incompatible embedding dimensions!")
#             print(f"   Current model: {EMBEDDING_MODEL}")
#             return []
#         raise

# def retrieve_relevant_memory(query: str, n_results=MAX_CONTEXT_TURNS):
#     global chat_collection
#     try:
#         query_embedding = embed_text(query)
#         results = chat_collection.query(
#             query_embeddings=[query_embedding],
#             n_results=n_results,
#             include=["documents", "distances"]
#         )
#         relevant_history = []
#         if results['documents'] and results['distances']:
#             for doc, dist in zip(results['documents'][0], results['distances'][0]):
#                 if dist < 0.7:
#                     relevant_history.append(doc)
#         return relevant_history
#     except Exception as e:
#         if "dimension" in str(e).lower():
#             print("⚠️ Embedding dimension mismatch. Recreating chat collection...")
#             try:
#                 chat_client.delete_collection(name="chat_memory")
#             except:
#                 pass
#             chat_collection = chat_client.create_collection(
#                 name="chat_memory", metadata={"hnsw:space": "cosine"})
#             return []
#         raise

# def build_rag_context(query: str):
#     """Combine only HIGHLY RELEVANT book RAG + chat memory."""
#     book_chunks = retrieve_book_rag(query)
#     chat_history = retrieve_relevant_memory(query)
    
#     context_parts = []
#     if book_chunks:
#         context_parts.append("📚 BOOK KNOWLEDGE (HIGHLY RELEVANT):\n" + "\n\n".join(book_chunks))
#     if chat_history:
#         context_parts.append("💬 PAST CONVERSATIONS (RELEVANT):\n" + "\n\n".join(chat_history))
    
#     if context_parts:
#         return "\n\n" + "="*50 + "\n\n".join(context_parts) + "\n\n" + "="*50
#     return None

# def get_books_for_api():
#     """Return book data for the API endpoint."""
#     if book_collection:
#         count = book_collection.count()
#         if count > 0:
#             return [{"book_id": "all", "title": "Indian Culture and Universal Values", "chunk_count": count}]
#     return []




# import chromadb
# from pathlib import Path
# import ollama

# # DATABASE PATHS
# CHROMA_CHAT_PATH = Path("chroma_memory_db")
# BOOK_DB_PATH = Path("book_rag_db")

# # Initialize Clients
# chat_client = chromadb.PersistentClient(path=str(CHROMA_CHAT_PATH))
# book_client = chromadb.PersistentClient(path=str(BOOK_DB_PATH))

# try:
#     book_collection = book_client.get_collection("book_content")
# except:
#     book_collection = None

# MODEL_NAME = "llama3:latest"
# EMBEDDING_MODEL = "nomic-embed-text:latest"

# # === CRITICAL FIX IS HERE ===
# def embed_text(text: str, task_type: str = "document"):
#     """
#     Wraps text with Nomic-specific prefixes.
#     task_type: 'search_query' for questions, 'search_document' for storage.
#     """
#     if "nomic" in EMBEDDING_MODEL:
#         prefix = "search_query: " if task_type == "query" else "search_document: "
#         if not text.startswith(prefix):
#             text = prefix + text
            
#     response = ollama.embeddings(model=EMBEDDING_MODEL, prompt=text)
#     return response['embedding']
# # ============================

# def get_or_create_chat_collection():
#     try:
#         return chat_client.get_collection(name="chat_memory")
#     except:
#         return chat_client.create_collection(name="chat_memory", metadata={"hnsw:space": "cosine"})

# chat_collection = get_or_create_chat_collection()

# def summarize_history(history_list: list):
#     if len(history_list) < 2: return "\n".join(history_list)
#     prompt = f"Summarize briefly:\n\n" + "\n".join(history_list)
#     return f"SUMMARY: {ollama.generate(model=MODEL_NAME, prompt=prompt)['response']}"

# def add_memory(user_text: str, assistant_text: str):
#     combined = f"User: {user_text}\nAssistant: {assistant_text}"
#     next_id = len(chat_collection.get().get("ids", [])) + 1
#     chat_collection.add(
#         embeddings=[embed_text(combined, task_type="document")],
#         documents=[combined],
#         metadatas=[{"type": "conversation_turn"}],
#         ids=[f"turn_{next_id}"]
#     )

# def retrieve_book_rag(query: str, n_results=5):
#     print(f"\n🔍 DEBUG: Searching DB for: '{query}'")
#     if not book_collection:
#         print("❌ DEBUG: book_collection is NONE.")
#         return []
    
#     # Use 'query' task type for searching
#     query_embed = embed_text(query, task_type="query")
    
#     results = book_collection.query(
#         query_embeddings=[query_embed], 
#         n_results=n_results,
#         include=["documents", "metadatas", "distances"]
#     )
    
#     count = len(results['documents'][0]) if results['documents'] else 0
#     print(f"✅ DEBUG: Found {count} raw matches in DB.")
    
#     relevant = []
#     if results['documents']:
#         for i in range(len(results['documents'][0])):
#             dist = results['distances'][0][i]
#             # Print distance to help debug
#             print(f"   - Chunk {i} distance: {dist:.4f}")
#             if dist < 0.85:
#                 relevant.append({
#                     "text": results['documents'][0][i],
#                     "id": results['metadatas'][0][i].get("chunk_id", "Unknown"),
#                     "score": dist
#                 })
#     return relevant

# def retrieve_relevant_memory(query: str):
#     q_embed = embed_text(query, task_type="query")
#     results = chat_collection.query(query_embeddings=[q_embed], n_results=3)
#     return results['documents'][0] if results['documents'] else []

# def build_rag_context(query: str):
#     book_res = retrieve_book_rag(query)
#     chat_hist = retrieve_relevant_memory(query)
    
#     context = []
#     if book_res:
#         txt = "\n\n".join([f"[Source: {x['id']}] {x['text']}" for x in book_res])
#         context.append("📖 MANDATORY TEXTBOOK MATERIAL:\n" + txt)
#     if chat_hist:
#         context.append("💬 HISTORY:\n" + summarize_history(chat_hist))
        
#     return ("\n\n".join(context) if context else None), book_res

# def get_books_for_api():
#     return [{"book_id": "all", "title": "Course Material", "chunk_count": book_collection.count()}] if book_collection else []

# def clear_chat_history(confirm_text=None):
#     if confirm_text == 'YES':
#         ids = chat_collection.get().get("ids", [])
#         if ids: chat_collection.delete(ids=ids)
#         return "✅ Cleared"
#     return "ℹ️ No action"



############ before multi syllabic embedding fix ############


import chromadb
from pathlib import Path
import ollama

# CONFIGURATION
MODEL_NAME = "llama3:latest"
EMBEDDING_MODEL = "nomic-embed-text:latest"

# 1. DATABASE PATHS MAP
# We now have a folder for EACH subject
DB_ROOT = Path("subject_dbs")
DB_MAP = {
    "rtl": DB_ROOT / "rtl_db",
    "python": DB_ROOT / "python_db",
    "maths": DB_ROOT / "maths_db",
    "english": DB_ROOT / "english_db"
}

CHROMA_CHAT_PATH = Path("chroma_memory_db")

# Initialize Chat Memory (Global)
chat_client = chromadb.PersistentClient(path=str(CHROMA_CHAT_PATH))

# 2. DYNAMIC CLIENT LOADING
# We will load the specific subject DB only when needed
def get_subject_collection(subject: str):
    """Loads the specific database for the requested subject."""
    if subject not in DB_MAP:
        print(f"❌ Error: Subject '{subject}' not found in DB_MAP")
        return None
        
    db_path = DB_MAP[subject]
    
    # Create the folder if it doesn't exist yet (prevents crashes)
    if not db_path.exists():
        db_path.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=str(db_path))
    try:
        # Note: We enforce 'cosine' distance for all subjects
        return client.get_or_create_collection(name="book_content", metadata={"hnsw:space": "cosine"})
    except Exception as e:
        print(f"⚠️ Error loading {subject} DB: {e}")
        return None

# Common Embedding Function
def embed_text(text: str, task_type: str = "document"):
    if "nomic" in EMBEDDING_MODEL:
        prefix = "search_query: " if task_type == "query" else "search_document: "
        if not text.startswith(prefix):
            text = prefix + text
    return ollama.embeddings(model=EMBEDDING_MODEL, prompt=text)['embedding']

def get_or_create_chat_collection():
    return chat_client.get_or_create_collection(name="chat_memory", metadata={"hnsw:space": "cosine"})

chat_collection = get_or_create_chat_collection()

# === MEMORY & HISTORY UTILS (Unchanged) ===
def get_recent_history(n_turns=2):
    try:
        all_data = chat_collection.get()
        ids = all_data['ids']
        if not ids: return []
        sorted_ids = sorted(ids, key=lambda x: int(x.split('_')[1]))
        recent_ids = sorted_ids[-n_turns:]
        recent_data = chat_collection.get(ids=recent_ids)
        id_doc_map = {id_: doc for id_, doc in zip(recent_data['ids'], recent_data['documents'])}
        return [id_doc_map[id_] for id_ in recent_ids]
    except: return []

def contextualize_query(user_query: str):
    history_docs = get_recent_history(n_turns=2)
    if not history_docs: return user_query
    
    prompt = f"""Conversation History:
{"\n".join(history_docs)}

Current Question: "{user_query}"

TASK: Rewrite the 'Current Question' to be a standalone search query.
CRITICAL RULES:
1. If the 'Current Question' uses pronouns (it, he, they, this) referring to the History, replace them with the specific noun.
2. If the 'Current Question' is a COMPLETELY NEW TOPIC (like switching from 'Integrity' to 'Python'), DO NOT combine them. Just return the 'Current Question' exactly as it is.

Output ONLY the rewritten question. NO extra text."""
    
    response = ollama.generate(model=MODEL_NAME, prompt=prompt)
    return response['response'].strip().replace('"', '')

def add_memory(user_text: str, assistant_text: str):
    combined = f"User: {user_text}\nAssistant: {assistant_text}"
    existing_ids = chat_collection.get()['ids']
    next_id = (max([int(x.split('_')[1]) for x in existing_ids]) + 1) if existing_ids else 1
    chat_collection.add(
        embeddings=[embed_text(combined, task_type="document")],
        documents=[combined],
        metadatas=[{"type": "conversation_turn"}],
        ids=[f"turn_{next_id}"]
    )

# === NEW: RETRIEVE FROM SPECIFIC SUBJECT ===
def retrieve_book_rag(query: str, subject: str, n_results=3):
    print(f"\n🔍 DEBUG: Searching '{subject}' DB for: '{query}'")
    
    collection = get_subject_collection(subject)
    if not collection or collection.count() == 0:
        print(f"⚠️ Warning: '{subject}' database is empty or missing.")
        return []
    
    query_embed = embed_text(query, task_type="query")
    results = collection.query(
        query_embeddings=[query_embed], 
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    
    relevant = []
    if results['documents']:
        for i in range(len(results['documents'][0])):
            dist = results['distances'][0][i]
            if dist < 0.85: # Cosine threshold
                relevant.append({
                    "text": results['documents'][0][i],
                    "id": results['metadatas'][0][i].get("chunk_id", "Unknown"),
                    "score": dist
                })
    return relevant

def build_rag_context(user_query: str, subject: str = "rtl"):
    # 1. Rewrite Query
    search_query = contextualize_query(user_query)
    
    # 2. Search TARGET Subject DB
    book_res = retrieve_book_rag(search_query, subject)
    
    context = []
    if book_res:
        txt = "\n\n".join([f"[Source: {x['id']}] {x['text']}" for x in book_res])
        context.append(f"📖 {subject.upper()} TEXTBOOK MATERIAL:\n" + txt)
    
    recent_history = get_recent_history(2)
    if recent_history:
         context.append("💬 RECENT HISTORY:\n" + "\n".join(recent_history))
        
    return ("\n\n".join(context) if context else None), book_res

def clear_chat_history(confirm_text=None):
    if confirm_text == 'YES':
        ids = chat_collection.get().get("ids", [])
        if ids: chat_collection.delete(ids=ids)
        return "✅ Cleared"
    return "ℹ️ No action"