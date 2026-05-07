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



############ before multi syllabic embedding fix is up ############


# import chromadb
# from pathlib import Path
# import ollama

# # CONFIGURATION
# MODEL_NAME = "llama3:latest"
# EMBEDDING_MODEL = "nomic-embed-text:latest"

# # 1. DATABASE PATHS MAP
# # We now have a folder for EACH subject
# DB_ROOT = Path("subject_dbs")
# DB_MAP = {
#     "rtl": DB_ROOT / "rtl_db",
#     "python": DB_ROOT / "python_db",
#     "maths": DB_ROOT / "maths_db",
#     "english": DB_ROOT / "english_db"
# }

# CHROMA_CHAT_PATH = Path("chroma_memory_db")

# # Initialize Chat Memory (Global)
# chat_client = chromadb.PersistentClient(path=str(CHROMA_CHAT_PATH))

# # 2. DYNAMIC CLIENT LOADING
# # We will load the specific subject DB only when needed
# def get_subject_collection(subject: str):
#     """Loads the specific database for the requested subject."""
#     if subject not in DB_MAP:
#         print(f"❌ Error: Subject '{subject}' not found in DB_MAP")
#         return None
        
#     db_path = DB_MAP[subject]
    
#     # Create the folder if it doesn't exist yet (prevents crashes)
#     if not db_path.exists():
#         db_path.mkdir(parents=True, exist_ok=True)

#     client = chromadb.PersistentClient(path=str(db_path))
#     try:
#         # Note: We enforce 'cosine' distance for all subjects
#         return client.get_or_create_collection(name="book_content", metadata={"hnsw:space": "cosine"})
#     except Exception as e:
#         print(f"⚠️ Error loading {subject} DB: {e}")
#         return None

# # Common Embedding Function
# def embed_text(text: str, task_type: str = "document"):
#     if "nomic" in EMBEDDING_MODEL:
#         prefix = "search_query: " if task_type == "query" else "search_document: "
#         if not text.startswith(prefix):
#             text = prefix + text
#     return ollama.embeddings(model=EMBEDDING_MODEL, prompt=text)['embedding']

# def get_or_create_chat_collection():
#     return chat_client.get_or_create_collection(name="chat_memory", metadata={"hnsw:space": "cosine"})

# chat_collection = get_or_create_chat_collection()

# # === MEMORY & HISTORY UTILS (Unchanged) ===
# def get_recent_history(n_turns=2):
#     try:
#         all_data = chat_collection.get()
#         ids = all_data['ids']
#         if not ids: return []
#         sorted_ids = sorted(ids, key=lambda x: int(x.split('_')[1]))
#         recent_ids = sorted_ids[-n_turns:]
#         recent_data = chat_collection.get(ids=recent_ids)
#         id_doc_map = {id_: doc for id_, doc in zip(recent_data['ids'], recent_data['documents'])}
#         return [id_doc_map[id_] for id_ in recent_ids]
#     except: return []

# def contextualize_query(user_query: str):
#     history_docs = get_recent_history(n_turns=2)
#     if not history_docs: return user_query
    
#     prompt = f"""Conversation History:
# {"\n".join(history_docs)}

# Current Question: "{user_query}"

# TASK: Rewrite the 'Current Question' to be a standalone search query.
# CRITICAL RULES:
# 1. If the 'Current Question' uses pronouns (it, he, they, this) referring to the History, replace them with the specific noun.
# 2. If the 'Current Question' is a COMPLETELY NEW TOPIC (like switching from 'Integrity' to 'Python'), DO NOT combine them. Just return the 'Current Question' exactly as it is.

# Output ONLY the rewritten question. NO extra text."""
    
#     response = ollama.generate(model=MODEL_NAME, prompt=prompt)
#     return response['response'].strip().replace('"', '')

# def add_memory(user_text: str, assistant_text: str):
#     combined = f"User: {user_text}\nAssistant: {assistant_text}"
#     existing_ids = chat_collection.get()['ids']
#     next_id = (max([int(x.split('_')[1]) for x in existing_ids]) + 1) if existing_ids else 1
#     chat_collection.add(
#         embeddings=[embed_text(combined, task_type="document")],
#         documents=[combined],
#         metadatas=[{"type": "conversation_turn"}],
#         ids=[f"turn_{next_id}"]
#     )

# # === NEW: RETRIEVE FROM SPECIFIC SUBJECT ===
# def retrieve_book_rag(query: str, subject: str, n_results=3):
#     print(f"\n🔍 DEBUG: Searching '{subject}' DB for: '{query}'")
    
#     collection = get_subject_collection(subject)
#     if not collection or collection.count() == 0:
#         print(f"⚠️ Warning: '{subject}' database is empty or missing.")
#         return []
    
#     query_embed = embed_text(query, task_type="query")
#     results = collection.query(
#         query_embeddings=[query_embed], 
#         n_results=n_results,
#         include=["documents", "metadatas", "distances"]
#     )
    
#     relevant = []
#     if results['documents']:
#         for i in range(len(results['documents'][0])):
#             dist = results['distances'][0][i]
#             if dist < 0.85: # Cosine threshold
#                 relevant.append({
#                     "text": results['documents'][0][i],
#                     "id": results['metadatas'][0][i].get("chunk_id", "Unknown"),
#                     "score": dist
#                 })
#     return relevant

# def build_rag_context(user_query: str, subject: str = "rtl"):
#     # 1. Rewrite Query
#     search_query = contextualize_query(user_query)
    
#     # 2. Search TARGET Subject DB
#     book_res = retrieve_book_rag(search_query, subject)
    
#     context = []
#     if book_res:
#         txt = "\n\n".join([f"[Source: {x['id']}] {x['text']}" for x in book_res])
#         context.append(f"📖 {subject.upper()} TEXTBOOK MATERIAL:\n" + txt)
    
#     recent_history = get_recent_history(2)
#     if recent_history:
#          context.append("💬 RECENT HISTORY:\n" + "\n".join(recent_history))
        
#     return ("\n\n".join(context) if context else None), book_res

# def clear_chat_history(confirm_text=None):
#     if confirm_text == 'YES':
#         ids = chat_collection.get().get("ids", [])
#         if ids: chat_collection.delete(ids=ids)
#         return "✅ Cleared"
#     return "ℹ️ No action"


#############  multi syllabic integration is up ############


############# DOWN CODE IS   contexualizing and history chat reading is removed and going to be optimized hopefully in the code below. in case of fire , the up code is best to use for now. #############

# import chromadb
# from pathlib import Path
# from ollama import Client

# # 1. EXPLICIT CLIENT & CONFIG
# ollama_client = Client(host='http://127.0.0.1:11434') 

# # Ensure this matches your download: qwen3:4b-instruct
# MODEL_NAME = "qwen3:4b-instruct"
# EMBEDDING_MODEL = "nomic-embed-text:latest"

# # 2. DATABASE PATHS
# DB_ROOT = Path("subject_dbs")
# DB_MAP = {
#     "rtl": DB_ROOT / "rtl_db",
#     "python": DB_ROOT / "python_db",
#     "maths": DB_ROOT / "maths_db",
#     "english": DB_ROOT / "english_db"
# }

# CHROMA_CHAT_PATH = Path("chroma_memory_db")

# # Global clients to prevent "re-opening" the DB on every message
# chat_client = chromadb.PersistentClient(path=str(CHROMA_CHAT_PATH))
# _subject_clients = {} 

# def get_subject_collection(subject: str):
#     if subject not in DB_MAP:
#         return None
        
#     if subject not in _subject_clients:
#         db_path = DB_MAP[subject]
#         if not db_path.exists():
#             db_path.mkdir(parents=True, exist_ok=True)
#         _subject_clients[subject] = chromadb.PersistentClient(path=str(db_path))

#     client = _subject_clients[subject]
#     try:
#         return client.get_or_create_collection(name="book_content", metadata={"hnsw:space": "cosine"})
#     except Exception as e:
#         print(f"⚠️ Error loading {subject} DB: {e}")
#         return None

# # --- 🚀 CRITICAL SPEED UPDATE ---
# def embed_text(text: str, task_type: str = "document"):
#     """Uses all 8 CPU threads to make database searching instant."""
#     if "nomic" in EMBEDDING_MODEL:
#         prefix = "search_query: " if task_type == "query" else "search_document: "
#         if not text.startswith(prefix):
#             text = prefix + text
    
#     # We add options here so the CPU doesn't 'lazy-load' the embeddings
#     response = ollama_client.embeddings(
#         model=EMBEDDING_MODEL, 
#         prompt=text,
#         options={"num_thread": 8} # <--- Force CPU power here too
#     )
#     return response['embedding']

# # 4. MEMORY & HISTORY UTILS
# def get_or_create_chat_collection():
#     return chat_client.get_or_create_collection(name="chat_memory", metadata={"hnsw:space": "cosine"})

# chat_collection = get_or_create_chat_collection()

# def get_recent_history(n_turns=2):
#     try:
#         all_data = chat_collection.get()
#         ids = all_data['ids']
#         if not ids: return []
#         sorted_ids = sorted(ids, key=lambda x: int(x.split('_')[1]))
#         recent_ids = sorted_ids[-n_turns:]
#         recent_data = chat_collection.get(ids=recent_ids)
#         id_doc_map = {id_: doc for id_, doc in zip(recent_data['ids'], recent_data['documents'])}
#         return [id_doc_map[id_] for id_ in recent_ids]
#     except: return []

# def add_memory(user_text: str, assistant_text: str):
#     # We wrap this in a try-block so memory errors never crash the main chat
#     try:
#         combined = f"User: {user_text}\nAssistant: {assistant_text}"
#         existing_ids = chat_collection.get()['ids']
#         next_id = (max([int(x.split('_')[1]) for x in existing_ids]) + 1) if existing_ids else 1
#         chat_collection.add(
#             embeddings=[embed_text(combined, task_type="document")],
#             documents=[combined],
#             metadatas=[{"type": "conversation_turn"}],
#             ids=[f"turn_{next_id}"]
#         )
#     except Exception as e:
#         print(f"⚠️ Memory save failed: {e}")

# # 5. RETRIEVAL & RAG
# def retrieve_book_rag(query: str, subject: str, n_results=3):
#     print(f"\n🔍 DEBUG: Searching '{subject}' DB for: '{query}'")
#     collection = get_subject_collection(subject)
#     if not collection or collection.count() == 0:
#         return []
    
#     query_embed = embed_text(query, task_type="query")
#     results = collection.query(
#         query_embeddings=[query_embed], 
#         n_results=n_results,
#         include=["documents", "metadatas", "distances"]
#     )
    
#     relevant = []
#     if results['documents'] and results['documents'][0]:
#         for i in range(len(results['documents'][0])):
#             dist = results['distances'][0][i]
#             # Threshold: 0.85 is good for nomic-embed
#             if dist < 0.85: 
#                 relevant.append({
#                     "text": results['documents'][0][i],
#                     "id": results['metadatas'][0][i].get("chunk_id", "Unknown"),
#                     "score": dist
#                 })
#     return relevant

# def build_rag_context(user_query: str, subject: str = "rtl"):
#     book_res = retrieve_book_rag(user_query, subject)
#     context = []
#     if book_res:
#         txt = "\n\n".join([f"[Source: {x['id']}] {x['text']}" for x in book_res])
#         context.append(f"📖 {subject.upper()} TEXTBOOK MATERIAL:\n" + txt)
    
#     recent_history = get_recent_history(2)
#     if recent_history:
#          context.append("💬 RECENT HISTORY:\n" + "\n".join(recent_history))
        
#     return ("\n\n".join(context) if context else None), book_res

# def clear_chat_history(confirm_text=None):
#     if confirm_text == 'YES':
#         ids = chat_collection.get().get("ids", [])
#         if ids: chat_collection.delete(ids=ids)
#         return "✅ Cleared"
#     return "ℹ️ No action"




######################## up code is before faiss ########################

#######################down code is after faiss #######################


# import chromadb
# from pathlib import Path
# from ollama import Client

# # 1. EXPLICIT CLIENT & CONFIG
# ollama_client = Client(host='http://127.0.0.1:11434') 

# MODEL_NAME = "qwen3:4b-instruct"
# EMBEDDING_MODEL = "nomic-embed-text:latest"

# # 2. DATABASE PATHS
# DB_ROOT = Path("subject_dbs")
# DB_MAP = {
#     "rtl": DB_ROOT / "rtl_db",
#     "python": DB_ROOT / "python_db",
#     "maths": DB_ROOT / "maths_db",
#     "english": DB_ROOT / "english_db"
# }

# _subject_clients = {} 

# def get_subject_collection(subject: str):
#     if subject not in DB_MAP:
#         return None
        
#     if subject not in _subject_clients:
#         db_path = DB_MAP[subject]
#         if not db_path.exists():
#             db_path.mkdir(parents=True, exist_ok=True)
#         _subject_clients[subject] = chromadb.PersistentClient(path=str(db_path))

#     client = _subject_clients[subject]
#     try:
#         return client.get_or_create_collection(name="book_content", metadata={"hnsw:space": "cosine"})
#     except Exception as e:
#         print(f"⚠️ Error loading {subject} DB: {e}")
#         return None

# def embed_text(text: str, task_type: str = "document"):
#     """Uses all 8 CPU threads to make database searching instant."""
#     if "nomic" in EMBEDDING_MODEL:
#         prefix = "search_query: " if task_type == "query" else "search_document: "
#         if not text.startswith(prefix):
#             text = prefix + text
    
#     response = ollama_client.embeddings(
#         model=EMBEDDING_MODEL, 
#         prompt=text,
#         options={"num_thread": 8},
#         keep_alive="24h" # Keeps the embedding model loaded instantly
#     )
#     return response['embedding']

# # 3. RETRIEVAL LOGIC
# # --- 🚀 UPDATED RETRIEVAL LOGIC ---
# def retrieve_book_rag(query: str, subject: str, n_results=3):
#     print(f"\n🔍 DEBUG: Searching '{subject}' DB for: '{query}'")
#     collection = get_subject_collection(subject)
#     if not collection or collection.count() == 0:
#         return []
    
#     query_embed = embed_text(query, task_type="query")
#     results = collection.query(
#         query_embeddings=[query_embed], 
#         n_results=n_results,
#         include=["documents", "metadatas", "distances"]
#     )
    
#     relevant = []
#     if results['documents'] and results['documents'][0]:
#         for i in range(len(results['documents'][0])):
#             dist = results['distances'][0][i]
            
#             # --- 💡 LOOSENED FILTER: 0.80 -> 0.85 ---
#             # This allows more "specific" matches (like names) to pass through.
#             if dist < 0.85: 
#                 relevant.append({
#                     "text": results['documents'][0][i],
#                     "id": results['metadatas'][0][i].get("chunk_id", "Unknown"),
#                     "topic": results['metadatas'][0][i].get("topic", "Reference"),
#                     "score": dist
#                 })
#     return relevant

# # 4. CONTEXT BUILDING (The "Never Lose Context" Engine)
# def build_rag_context(user_query: str, chat_history: list, subject: str = "rtl"):
#     """
#     Combines Retrieval Augmented Generation with real-time Chat History.
#     chat_history expected format: [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
#     """
#     # 1. Get Textbook Material
#     book_res = retrieve_book_rag(user_query, subject)
    
#     context_parts = []
    
#     if book_res:
#         txt = "\n\n".join([f"[Source: {x['topic']}] {x['text']}" for x in book_res])
#         context_parts.append(f"📖 {subject.upper()} TEXTBOOK MATERIAL:\n" + txt)
    
#     # 2. Format Chat History (Sliding Window: Last 5 turns)
#     if chat_history:
#         history_text = ""
#         for turn in chat_history[-5:]: # Keep it light, keep it fast
#             role = "Student" if turn['role'] == 'user' else "ALIN1"
#             history_text += f"{role}: {turn['content']}\n"
        
#         context_parts.append("💬 RECENT CONVERSATION LOG:\n" + history_text)
        
#     final_context = "\n\n".join(context_parts) if context_parts else None
    
#     return final_context, book_res

# def classify_intent(user_query: str) -> str:
#     """
#     Quickly determines if the user is seeking textbook knowledge 
#     or just having a casual conversation.
#     """
#     # Simple keyword bypass for ultra-fast response on common greetings
#     greetings = {"hi", "hello", "hey", "how are you", "who are you", "alin1"}
#     if user_query.lower().strip().strip('?!.') in greetings:
#         return "CHAT"

#     # Fast LLM check for more complex intent
#     prompt = f"Categorize this user query as 'KNOWLEDGE' (if asking about RTL, Python, Math, or specific facts) or 'CHAT' (if small talk/greetings). Query: {user_query}\nCategory:"
    
#     response = ollama_client.generate(
#         model=MODEL_NAME, 
#         prompt=prompt,
#         options={"num_predict": 2, "temperature": 0} # Extremely fast, 1-2 tokens only
#     )
    
#     return "KNOWLEDGE" if "KNOWLEDGE" in response['response'].upper() else "CHAT"






###################### down code is convo classification and intent detection added (chit chat) ######################



# import chromadb
# import xml.etree.ElementTree as ET
# from pathlib import Path
# from ollama import Client
# import os
# print(f"🚀 ALIN1 IS RUNNING RAG_CORE FROM: {os.path.abspath(__file__)}")

# # 1. CLIENT CONFIGURATION
# ollama_client = Client(host='http://127.0.0.1:11434') 

# MODEL_NAME = "qwen3:4b-instruct"
# EMBEDDING_MODEL = "nomic-embed-text:latest"

# # 2. DATABASE SETUP
# DB_ROOT = Path("subject_dbs")
# DB_MAP = {
#     "rtl": DB_ROOT / "rtl_db",
#     "python": DB_ROOT / "python_db",
#     "maths": DB_ROOT / "maths_db",
#     "english": DB_ROOT / "english_db"
# }

# _subject_clients = {} 

# def get_subject_collection(subject: str):
#     if subject not in DB_MAP:
#         return None
        
#     if subject not in _subject_clients:
#         db_path = DB_MAP[subject]
#         db_path.mkdir(parents=True, exist_ok=True)
#         _subject_clients[subject] = chromadb.PersistentClient(path=str(db_path))

#     client = _subject_clients[subject]
#     try:
#         return client.get_or_create_collection(name="book_content", metadata={"hnsw:space": "cosine"})
#     except Exception as e:
#         print(f"⚠️ DB Error: {e}")
#         return None

# # --- 🚀 PERFORMANCE: INSTANT EMBEDDINGS ---
# def embed_text(text: str, task_type: str = "document"):
#     if "nomic" in EMBEDDING_MODEL:
#         prefix = "search_query: " if task_type == "query" else "search_document: "
#         if not text.startswith(prefix):
#             text = prefix + text
    
#     response = ollama_client.embeddings(
#         model=EMBEDDING_MODEL, 
#         prompt=text,
#         options={"num_thread": 8},
#         keep_alive="24h" # Keeps embedding model in VRAM for zero-lag search
#     )
#     return response['embedding']

# # --- 🎯 INTENT ROUTER: CHIT-CHAT BYPASS ---
# def classify_intent(user_query: str) -> str:
#     """Detects if we need RAG or just a quick chat."""
#     clean_query = user_query.lower().strip().strip('?!.')

#     # 1. Subject Keywords (Force Knowledge)
#     knowledge_triggers = ["rtl", "cfsr", "integrity", "karuna", "values", "practitioner", "overwhelm", "what is"]
#     if any(trigger in clean_query for trigger in knowledge_triggers):
#         print(f"🔍 DEBUG: INTENT OVERRIDE -> KNOWLEDGE (Keyword Match)")
#         return "KNOWLEDGE"

#     # 2. Pure Greetings (Force Chat)
#     greetings = {"hi", "hello", "hey", "how are you", "who are you", "alin1", "thanks", "thank you"}
#     if clean_query in greetings:
#         return "CHAT"

#     # 3. Fallback to LLM
#     prompt = f"Categorize as 'KNOWLEDGE' (syllabus/facts) or 'CHAT' (greeting/small talk). Query: {user_query}\nCategory:"
#     response = ollama_client.generate(
#         model=MODEL_NAME, 
#         prompt=prompt,
#         options={"num_predict": 2, "temperature": 0} 
#     )
#     return "KNOWLEDGE" if "KNOWLEDGE" in response['response'].upper() else "CHAT"


# # --- 🧩 POML ASSEMBLER: STRUCTURED PROMPTS ---
# def get_poml_prompt(subject: str) -> str:
#     """Assembles the XML-based system prompt from our .poml files using absolute paths."""
#     try:
#         # 1. Get the directory where rag_core.py is located
#         current_dir = Path(__file__).parent.absolute()
        
#         # 2. Point to the prompts folder (Assumes it is one level up from backend/)
#         prompts_dir = current_dir / "prompts"
        
#         # 3. Load Base Directives
#         base_path = prompts_dir / "alin1_base.poml"
#         base_tree = ET.parse(str(base_path))
#         directives = ET.tostring(base_tree.find(".//directives"), encoding='unicode')

#         # 4. Load Persona
#         persona_path = prompts_dir / "personas.poml"
#         persona_tree = ET.parse(str(persona_path))
#         persona_node = persona_tree.find(f".//persona[@id='{subject}']")
#         persona_text = persona_node.text.strip() if persona_node is not None else "You are ALIN1."

#         return f"<poml version='1.0'>\n<system>\n<persona>{persona_text}</persona>\n{directives}\n</system>\n</poml>"
#     except Exception as e:
#         print(f"POML Error: {e}")
#         return "You are ALIN1, a specialized AI Tutor. strictly use textbook material only."

# # --- 📖 RETRIEVAL LOGIC ---
# def retrieve_book_rag(query: str, subject: str, n_results=3):
#     collection = get_subject_collection(subject)
#     if not collection or collection.count() == 0:
#         return []
    
#     query_embed = embed_text(query, task_type="query")
#     results = collection.query(
#         query_embeddings=[query_embed], 
#         n_results=n_results,
#         include=["documents", "metadatas", "distances"]
#     )
    
#     relevant = []
#     if results['documents'] and results['documents'][0]:
#         for i in range(len(results['documents'][0])):
#             if results['distances'][0][i] < 0.85: # Tuned distance threshold
#                 relevant.append({
#                     "text": results['documents'][0][i],
#                     "id": results['metadatas'][0][i].get("chunk_id", "Unknown"),
#                     "topic": results['metadatas'][0][i].get("topic", "Reference")
#                 })
#     return relevant

# # --- 🧠 CONTEXT ENGINE ---
# def build_rag_context(user_query: str, chat_history: list, subject: str = "rtl"):
#     """Orchestrates Intent -> RAG (if needed) -> POML System Prompt."""
    
#     # 1. Classify Intent
#     intent = classify_intent(user_query)
    
#     # 2. Conditional Retrieval (Save time if just chatting)
#     book_res = []
#     if intent == "KNOWLEDGE":
#         book_res = retrieve_book_rag(user_query, subject)
    
#     # 3. Build context parts
#     context_parts = []
#     if book_res:
#         txt = "\n\n".join([f"[Source: {x['topic']}] {x['text']}" for x in book_res])
#         context_parts.append(f"📖 {subject.upper()} TEXTBOOK MATERIAL:\n{txt}")
    
#     # 4. Handle History (Last 5 turns)
#     if chat_history:
#         hist = "\n".join([f"{'Student' if t['role']=='user' else 'ALIN1'}: {t['content']}" for t in chat_history[-5:]])
#         context_parts.append(f"💬 RECENT CONVERSATION LOG:\n{hist}")
        
#     final_context = "\n\n".join(context_parts) if context_parts else None
    
#     # 5. Get the POML System Prompt
#     system_prompt = get_poml_prompt(subject)
    
#     return system_prompt, final_context, book_res
#     return system_prompt, final_context, book_res





##### upcode is 05night & 06 morning before touching code


# import chromadb
# import xml.etree.ElementTree as ET
# from pathlib import Path
# from ollama import Client
# import os
# print(f"🚀 ALIN1 IS RUNNING RAG_CORE FROM: {os.path.abspath(__file__)}")

# # 1. CLIENT CONFIGURATION
# ollama_client = Client(host='http://127.0.0.1:11434') 

# MODEL_NAME = "qwen3:4b-instruct"
# EMBEDDING_MODEL = "nomic-embed-text:latest"

# # 2. DATABASE SETUP
# DB_ROOT = Path("subject_dbs")
# DB_MAP = {
#     "rtl": DB_ROOT / "rtl_db",
#     "python": DB_ROOT / "python_db",
#     "maths": DB_ROOT / "maths_db",
#     "english": DB_ROOT / "english_db"
# }

# _subject_clients = {} 

# def get_subject_collection(subject: str):
#     if subject not in DB_MAP:
#         return None
        
#     if subject not in _subject_clients:
#         db_path = DB_MAP[subject]
#         db_path.mkdir(parents=True, exist_ok=True)
#         _subject_clients[subject] = chromadb.PersistentClient(path=str(db_path))

#     client = _subject_clients[subject]
#     try:
#         return client.get_or_create_collection(name="book_content", metadata={"hnsw:space": "cosine"})
#     except Exception as e:
#         print(f"⚠️ DB Error: {e}")
#         return None

# # --- 🚀 PERFORMANCE: INSTANT EMBEDDINGS ---
# def embed_text(text: str, task_type: str = "document"):
#     if "nomic" in EMBEDDING_MODEL:
#         prefix = "search_query: " if task_type == "query" else "search_document: "
#         if not text.startswith(prefix):
#             text = prefix + text
    
#     response = ollama_client.embeddings(
#         model=EMBEDDING_MODEL, 
#         prompt=text,
#         options={"num_thread": 8},
#         keep_alive="24h" # Keeps embedding model in VRAM for zero-lag search
#     )
#     return response['embedding']

# # --- 🎯 INTENT ROUTER: CHIT-CHAT BYPASS ---
# def classify_intent(user_query: str) -> str:
#     """Detects if we need RAG or just a quick chat."""
#     clean_query = user_query.lower().strip().strip('?!.')

#     # 1. Subject Keywords (Force Knowledge)
#     knowledge_triggers = ["rtl", "cfsr", "integrity", "karuna", "values", "practitioner", "overwhelm", "what is"]
#     if any(trigger in clean_query for trigger in knowledge_triggers):
#         print(f"🔍 DEBUG: INTENT OVERRIDE -> KNOWLEDGE (Keyword Match)")
#         return "KNOWLEDGE"

#     # 2. Pure Greetings (Force Chat)
#     greetings = {"hi", "hello", "hey", "how are you", "who are you", "alin1", "thanks", "thank you"}
#     if clean_query in greetings:
#         return "CHAT"

#     # 3. Fallback to LLM
#     prompt = f"Categorize as 'KNOWLEDGE' (syllabus/facts) or 'CHAT' (greeting/small talk). Query: {user_query}\nCategory:"
#     response = ollama_client.generate(
#         model=MODEL_NAME, 
#         prompt=prompt,
#         options={"num_predict": 2, "temperature": 0} 
#     )
#     return "KNOWLEDGE" if "KNOWLEDGE" in response['response'].upper() else "CHAT"


# # --- 🧩 POML ASSEMBLER: STRUCTURED PROMPTS ---
# def get_poml_prompt(subject: str) -> str:
#     """Assembles the XML-based system prompt from our .poml files using absolute paths."""
#     try:
#         # 1. Get the directory where rag_core.py is located
#         current_dir = Path(__file__).parent.absolute()
        
#         # 2. Point to the prompts folder (Assumes it is one level up from backend/)
#         prompts_dir = current_dir / "prompts"
        
#         # 3. Load Base Directives
#         base_path = prompts_dir / "alin1_base.poml"
#         base_tree = ET.parse(str(base_path))
#         directives = ET.tostring(base_tree.find(".//directives"), encoding='unicode')

#         # 4. Load Persona
#         persona_path = prompts_dir / "personas.poml"
#         persona_tree = ET.parse(str(persona_path))
#         persona_node = persona_tree.find(f".//persona[@id='{subject}']")
#         persona_text = persona_node.text.strip() if persona_node is not None else "You are ALIN1."

#         return f"<poml version='1.0'>\n<system>\n<persona>{persona_text}</persona>\n{directives}\n</system>\n</poml>"
#     except Exception as e:
#         print(f"POML Error: {e}")
#         return "You are ALIN1, a specialized AI Tutor. strictly use textbook material only."

# # --- 📖 RETRIEVAL LOGIC ---
# def retrieve_book_rag(query: str, subject: str, n_results=3):
#     collection = get_subject_collection(subject)
#     if not collection or collection.count() == 0:
#         return []
    
#     query_embed = embed_text(query, task_type="query")
#     results = collection.query(
#         query_embeddings=[query_embed], 
#         n_results=n_results,
#         include=["documents", "metadatas", "distances"]
#     )
    
#     relevant = []
#     if results['documents'] and results['documents'][0]:
#         for i in range(len(results['documents'][0])):
#             if results['distances'][0][i] < 0.85: # Tuned distance threshold
#                 relevant.append({
#                     "text": results['documents'][0][i],
#                     "id": results['metadatas'][0][i].get("chunk_id", "Unknown"),
#                     "topic": results['metadatas'][0][i].get("topic", "Reference")
#                 })
#     return relevant

# # --- 🧠 CONTEXT ENGINE ---
# def build_rag_context(user_query: str, chat_history: list, subject: str = "rtl"):
#     """Orchestrates Intent -> RAG (if needed) -> POML System Prompt."""
    
#     # 1. Classify Intent
#     intent = classify_intent(user_query)
    
#     # 2. Conditional Retrieval (Save time if just chatting)
#     book_res = []
#     if intent == "KNOWLEDGE":
#         # Query Enhancer: Fix acronym casing for the Vector DB
#         search_query = user_query.replace("cfsr", "CFSR").replace("rtl", "RTL")
#         book_res = retrieve_book_rag(search_query, subject)
    
#     # 3. Build context parts
#     context_parts = []
#     if book_res:
#         txt = "\n\n".join([f"[Source: {x['topic']}] {x['text']}" for x in book_res])
#         context_parts.append(f"📖 {subject.upper()} TEXTBOOK MATERIAL:\n{txt}")
    
#     # 4. Handle History (Last 5 turns)
#     if chat_history:
#         hist = "\n".join([f"{'Student' if t['role']=='user' else 'ALIN1'}: {t['content']}" for t in chat_history[-5:]])
#         context_parts.append(f"💬 RECENT CONVERSATION LOG:\n{hist}")
        
#     final_context = "\n\n".join(context_parts) if context_parts else None
    
#     # 5. Get the POML System Prompt
#     system_prompt = get_poml_prompt(subject)
    
#     return system_prompt, final_context, book_res



############# down code is faq ##########


import chromadb
import xml.etree.ElementTree as ET
from pathlib import Path
from ollama import Client
import os
print(f"🚀 ALIN1 IS RUNNING RAG_CORE FROM: {os.path.abspath(__file__)}")

# 1. CLIENT CONFIGURATION
ollama_client = Client(host='http://127.0.0.1:11434') 

MODEL_NAME = "qwen3:4b-instruct"
EMBEDDING_MODEL = "nomic-embed-text:latest"

# 2. DATABASE SETUP
DB_ROOT = Path("subject_dbs")
DB_MAP = {
    "rtl": DB_ROOT / "rtl_db",
    "python": DB_ROOT / "python_db",
    "maths": DB_ROOT / "maths_db",
    "english": DB_ROOT / "english_db"
}

_subject_clients = {} 

# --- ⚡ FAST-PATH FAQ LOOKUP TABLE ---
# Maps exact queries to specific ChromaDB chunk IDs.
# Bypasses the Embedding model and FAISS vector search entirely.
FAQ_CACHE = {
    "what is cfsr": [
        "Section 26", # This is the main CFSR model chunk
        "Section 27"  # This contains the CFSR exercise
    ],
    "what is integrity": [
        "Section 26"  # This chunk covers both Integrity and CFSR
    ],
    "who is the author": [
        "Section 132" # The closest match found for author/case study
    ]
}

def get_subject_collection(subject: str):
    if subject not in DB_MAP:
        return None
        
    if subject not in _subject_clients:
        db_path = DB_MAP[subject]
        db_path.mkdir(parents=True, exist_ok=True)
        _subject_clients[subject] = chromadb.PersistentClient(path=str(db_path))

    client = _subject_clients[subject]
    try:
        return client.get_or_create_collection(name="book_content", metadata={"hnsw:space": "cosine"})
    except Exception as e:
        print(f"⚠️ DB Error: {e}")
        return None

# --- 🚀 PERFORMANCE: INSTANT EMBEDDINGS ---
def embed_text(text: str, task_type: str = "document"):
    if "nomic" in EMBEDDING_MODEL:
        prefix = "search_query: " if task_type == "query" else "search_document: "
        if not text.startswith(prefix):
            text = prefix + text
    
    response = ollama_client.embeddings(
        model=EMBEDDING_MODEL, 
        prompt=text,
        options={"num_thread": 8},
        keep_alive="24h" # Keeps embedding model in VRAM for zero-lag search
    )
    return response['embedding']

# --- 🎯 INTENT ROUTER: CHIT-CHAT BYPASS ---
def classify_intent(user_query: str) -> str:
    """Detects if we need RAG or just a quick chat."""
    clean_query = user_query.lower().strip().strip('?!.')

    # 1. Subject Keywords (Force Knowledge)
    knowledge_triggers = ["rtl", "cfsr", "integrity", "karuna", "values", "practitioner", "overwhelm", "what is"]
    if any(trigger in clean_query for trigger in knowledge_triggers):
        print(f"🔍 DEBUG: INTENT OVERRIDE -> KNOWLEDGE (Keyword Match)")
        return "KNOWLEDGE"

    # 2. Pure Greetings (Force Chat)
    greetings = {"hi", "hello", "hey", "how are you", "who are you", "alin1", "thanks", "thank you"}
    if clean_query in greetings:
        return "CHAT"

    # 3. Fallback to LLM
    prompt = f"Categorize as 'KNOWLEDGE' (syllabus/facts) or 'CHAT' (greeting/small talk). Query: {user_query}\nCategory:"
    response = ollama_client.generate(
        model=MODEL_NAME, 
        prompt=prompt,
        options={"num_predict": 2, "temperature": 0} 
    )
    return "KNOWLEDGE" if "KNOWLEDGE" in response['response'].upper() else "CHAT"


# --- 🧩 POML ASSEMBLER: STRUCTURED PROMPTS ---
def get_poml_prompt(subject: str) -> str:
    """Assembles the XML-based system prompt from our .poml files using absolute paths."""
    try:
        # 1. Get the directory where rag_core.py is located
        current_dir = Path(__file__).parent.absolute()
        
        # 2. Point to the prompts folder (Assumes it is one level up from backend/)
        prompts_dir = current_dir / "prompts"
        
        # 3. Load Base Directives
        base_path = prompts_dir / "alin1_base.poml"
        base_tree = ET.parse(str(base_path))
        directives = ET.tostring(base_tree.find(".//directives"), encoding='unicode')

        # 4. Load Persona
        persona_path = prompts_dir / "personas.poml"
        persona_tree = ET.parse(str(persona_path))
        persona_node = persona_tree.find(f".//persona[@id='{subject}']")
        persona_text = persona_node.text.strip() if persona_node is not None else "You are ALIN1."

        return f"<poml version='1.0'>\n<system>\n<persona>{persona_text}</persona>\n{directives}\n</system>\n</poml>"
    except Exception as e:
        print(f"POML Error: {e}")
        return "You are ALIN1, a specialized AI Tutor. strictly use textbook material only."

# --- 📖 RETRIEVAL LOGIC (BYPASS & VECTOR) ---

def retrieve_faq_direct(chunk_ids: list, subject: str):
    """Bypasses vector search and fetches exact chunks by metadata chunk_id."""
    collection = get_subject_collection(subject)
    if not collection:
        return []
    
    # --- THE FIX: Search inside the metadata ('where' clause) ---
    results = collection.get(
        where={"chunk_id": {"$in": chunk_ids}}
    )
    
    relevant = []
    # Check if we actually found documents
    if results and results.get('documents') and len(results['documents']) > 0:
        for i in range(len(results['documents'])):
            relevant.append({
                "text": results['documents'][i],
                "id": results['metadatas'][i].get("chunk_id", "Unknown ID"),
                "topic": results['metadatas'][i].get("topic", "FAQ Fast-Match")
            })
    else:
        print(f"⚠️ BYPASS FAILED: Could not find these chunk_ids in metadata: {chunk_ids}")
        
    return relevant

def retrieve_book_rag(query: str, subject: str, n_results=3):
    """Standard Vector Math Search."""
    collection = get_subject_collection(subject)
    if not collection or collection.count() == 0:
        return []
    
    query_embed = embed_text(query, task_type="query")
    results = collection.query(
        query_embeddings=[query_embed], 
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    
    relevant = []
    if results['documents'] and results['documents'][0]:
        for i in range(len(results['documents'][0])):
            if results['distances'][0][i] < 0.85: # Tuned distance threshold
                relevant.append({
                    "text": results['documents'][0][i],
                    "id": results['metadatas'][0][i].get("chunk_id", "Unknown"),
                    "topic": results['metadatas'][0][i].get("topic", "Reference")
                })
    return relevant

# --- 🧠 CONTEXT ENGINE ---
# --- 🧠 CONTEXT ENGINE ---
def build_rag_context(user_query: str, chat_history: list, subject: str = "rtl"):
    """Orchestrates Intent -> RAG (if needed) -> POML System Prompt."""
    
    # 1. Classify Intent
    intent = classify_intent(user_query)
    clean_query = user_query.lower().strip().strip('?!.')
    
    is_faq = False # <-- NEW FLAG
    
    # 2. Conditional Retrieval (Save time if just chatting)
    book_res = []
    if intent == "KNOWLEDGE":
        
        # --- THE BYPASS CHECK ---
        if clean_query in FAQ_CACHE:
            print(f"⚡ FAQ BYPASS ACTIVATED FOR: '{clean_query}'")
            book_res = retrieve_faq_direct(FAQ_CACHE[clean_query], subject)
            is_faq = True # <-- SET THE FLAG TO TRUE
            
        # --- STANDARD VECTOR SEARCH ---
        else:
            search_query = user_query.replace("cfsr", "CFSR").replace("rtl", "RTL")
            book_res = retrieve_book_rag(search_query, subject)
    
    # 3. Build context parts
    context_parts = []
    if book_res:
        txt = "\n\n".join([f"[Source: {x['topic']}] {x['text']}" for x in book_res])
        context_parts.append(f"📖 {subject.upper()} TEXTBOOK MATERIAL:\n{txt}")
    
    # 4. Handle History (Last 5 turns)
    if chat_history:
        hist = "\n".join([f"{'Student' if t['role']=='user' else 'ALIN1'}: {t['content']}" for t in chat_history[-5:]])
        context_parts.append(f"💬 RECENT CONVERSATION LOG:\n{hist}")
        
    final_context = "\n\n".join(context_parts) if context_parts else None
    
    # 5. Get the POML System Prompt
    system_prompt = get_poml_prompt(subject)
    
    # <-- RETURN 4 VARIABLES INSTEAD OF 3 -->
    return system_prompt, final_context, book_res, is_faq