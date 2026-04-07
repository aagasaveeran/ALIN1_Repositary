# # from fastapi import FastAPI, Query
# # from fastapi.middleware.cors import CORSMiddleware
# # from sse_starlette.sse import EventSourceResponse
# # import json
# # import sys
# # import os

# # # Import your existing RAG code
# # from rag_core import (
# #     build_rag_context,
# #     add_memory,
# #     get_books_for_api,
# #     clear_chat_history
# # )

# # app = FastAPI(title="RAG Chat API")

# # # Allow CORS
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # @app.get("/books")
# # def get_books():
# #     return get_books_for_api()

# # @app.get("/chat/stream")
# # async def stream_chat(message: str = Query(...), book_id: str = Query("")):
# #     async def event_generator():
# #         try:
# #             # Build RAG context using your existing function
# #             rag_context = build_rag_context(message)
            
# #             # Prepare messages for Llama3
# #             if rag_context:
# #                 system_prompt = f"""You are an expert tutor using RAG.

# # IMPORTANT RULES:
# # 1. Answer ONLY using the RAG context provided below
# # 2. If the context doesn't contain the answer, say "I don't have that information."
# # 3. Quote directly from the book when possible
# # 4. Do NOT make up information

# # RAG CONTEXT:
# # {rag_context}

# # Answer the question "{message}" using ONLY the above context:"""
# #             else:
# #                 system_prompt = """NO RELEVANT CONTEXT FOUND.
# # You must say: "I don't have relevant information from the book or our conversations about this topic."

# # Do NOT answer with general knowledge."""
            
# #             messages = [
# #                 {"role": "system", "content": system_prompt},
# #                 {"role": "user", "content": message}
# #             ]
            
# #             # Stream from Ollama
# #             import ollama
# #             full_response = ""
# #             stream = ollama.chat(model="llama3:latest", messages=messages, stream=True)
            
# #             for chunk in stream:
# #                 if 'message' in chunk and 'content' in chunk['message']:
# #                     token = chunk['message']['content']
# #                     if token:
# #                         full_response += token
# #                         yield json.dumps({"token": token})
            
# #             # Save to memory
# #             add_memory(message, full_response)
# #             yield json.dumps({"done": True})
            
# #         except Exception as e:
# #             yield json.dumps({"error": str(e)})

# #     return EventSourceResponse(event_generator())

# # @app.post("/clear")
# # async def clear_memory():
# #     result = clear_chat_history('YES')
# #     return {"status": result}

# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run(app, host="0.0.0.0", port=8000)



# ############################# before gemini is up #############################







# # from fastapi import FastAPI, Query
# # from fastapi.middleware.cors import CORSMiddleware
# # from sse_starlette.sse import EventSourceResponse
# # import json
# # import sys
# # import os

# # # Import your existing RAG code
# # from rag_core import (
# #     build_rag_context,
# #     add_memory,
# #     get_books_for_api,
# #     clear_chat_history
# # )

# # app = FastAPI(title="ALIN1 RAG Chat API")

# # # Allow CORS
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # @app.get("/books")
# # def get_books():
# #     return get_books_for_api()

# # @app.get("/chat/stream")
# # async def stream_chat(message: str = Query(...), book_id: str = Query("")):
# #     async def event_generator():
# #         try:
# #             # 1. Build RAG context using your existing function
# #             rag_context = build_rag_context(message)
            
# #             # 2. Prepare System Prompt with Chain of Thought (Step 1 Modification)
# #             if rag_context:
# #                 system_prompt = f"""You are ALIN1, an expert academic tutor specializing in Indian Culture and Universal Values.

# # YOUR GOAL:
# # Provide a structured, accurate, and educational answer based ONLY on the context provided.

# # INSTRUCTIONS:
# # 1. **Analyze:** First, scan the "RAG CONTEXT" below to find the specific answer.
# # 2. **Verify:** If the context matches the question, formulate your answer.
# # 3. **Refuse:** If the context is empty or irrelevant, strictly say: "I checked my library, but I don't have specific information on that topic in the provided text."
# # 4. **Cite:** When mentioning specific concepts, refer to them as "according to the text."

# # RAG CONTEXT:
# # {rag_context}

# # User Question: "{message}"

# # Now, provide a clear, structured response (use bullet points if helpful):"""
# #             else:
# #                 system_prompt = """You are ALIN1.
# # The user asked a question, but we found NO matching information in the book database.
# # Politely inform the user that this specific topic is not covered in your current study material.
# # Do not attempt to answer from outside knowledge."""
            
# #             messages = [
# #                 {"role": "system", "content": system_prompt},
# #                 {"role": "user", "content": message}
# #             ]
            
# #             # 3. Stream from Ollama
# #             import ollama
# #             full_response = ""
# #             stream = ollama.chat(model="llama3:latest", messages=messages, stream=True)
            
# #             for chunk in stream:
# #                 if 'message' in chunk and 'content' in chunk['message']:
# #                     token = chunk['message']['content']
# #                     if token:
# #                         full_response += token
# #                         yield json.dumps({"token": token})
            
# #             # 4. Save to memory
# #             add_memory(message, full_response)
# #             yield json.dumps({"done": True})
            
# #         except Exception as e:
# #             # Yield error in a format the frontend expects
# #             yield json.dumps({"error": str(e)})

# #     return EventSourceResponse(event_generator())

# # @app.post("/clear")
# # async def clear_memory():
# #     result = clear_chat_history('YES')
# #     return {"status": result}

# # if __name__ == "__main__":
# #     import uvicorn
# #     # Hot reload is useful for development
# #     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)









# # from fastapi import FastAPI, Query
# # from fastapi.middleware.cors import CORSMiddleware
# # from sse_starlette.sse import EventSourceResponse
# # import json
# # import uvicorn
# # from rag_core import build_rag_context, add_memory, get_books_for_api, clear_chat_history, MODEL_NAME
# # import ollama

# # app = FastAPI(title="ALIN1 RAG API")

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # @app.get("/books")
# # def get_books():
# #     return get_books_for_api()

# # @app.get("/chat/stream")
# # async def stream_chat(message: str = Query(...)):
# #     async def event_generator():
# #         try:
# #             rag_context = build_rag_context(message)
# #             if rag_context:
# #                 system_prompt = f"You are an expert academic tutor. Answer ONLY using this context:\n{rag_context}"
# #             else:
# #                 system_prompt = "No relevant context found. Inform the user you only know about 'Indian Culture and Universal Values'."
            
# #             messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": message}]
# #             full_response = ""
# #             stream = ollama.chat(model=MODEL_NAME, messages=messages, stream=True)
            
# #             for chunk in stream:
# #                 if 'message' in chunk and 'content' in chunk['message']:
# #                     token = chunk['message']['content']
# #                     full_response += token
# #                     yield json.dumps({"token": token})
            
# #             add_memory(message, full_response)
# #             yield json.dumps({"done": True})
# #         except Exception as e:
# #             yield json.dumps({"error": str(e)})

# #     return EventSourceResponse(event_generator())

# # if __name__ == "__main__":
# #     uvicorn.run(app, host="0.0.0.0", port=8000)



# ######################THE DOWN CODE IS WOKRING FAST STREAMING BUT HALLUCINATES AND DOES NOT KNOW ANYTHING#####################

# # from fastapi import FastAPI, Query
# # from fastapi.middleware.cors import CORSMiddleware
# # from sse_starlette.sse import EventSourceResponse
# # import json
# # import ollama
# # import uvicorn

# # # Import logic from rag_core
# # from rag_core import (
# #     build_rag_context,
# #     add_memory,
# #     get_books_for_api,
# #     clear_chat_history,
# #     MODEL_NAME
# # )

# # app = FastAPI(title="ALIN1 AI Tutor System")

# # # Configure CORS for Angular (Port 4200)
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # @app.get("/books")
# # def get_books():
# #     return get_books_for_api()

# # @app.get("/chat/stream")
# # async def stream_chat(message: str = Query(...)):
# #     async def event_generator():
# #         try:
# #             # 1. Retrieve the context AND the source metadata
# #             rag_context, sources = build_rag_context(message)
            
# #             # 2. Send the sources to the UI first
# #             if sources:
# #                 source_ids = [str(s['id']) for s in sources]
# #                 yield json.dumps({"sources": source_ids})
            
# #             # 3. THE MASTER SYSTEM PROMPT
# #             if rag_context:
# #                 system_prompt = f"""You are ALIN1, an expert academic tutor for 'Indian Culture and Universal Values'.

# # CORE MISSION:
# # Help students understand course material using ONLY the provided context.

# # STRICT GUIDELINES:
# # 1. USE CONTEXT: Answer based ONLY on the 'MANDATORY COURSE TEXTBOOK MATERIAL' below.
# # 2. REFUSE OUTSIDE INFO: If asked about topics not in the context, say: "I am specialized in Indian Culture and Universal Values. My current library does not cover that topic."
# # 3. STYLE: Use bullet points and bold text for clarity.
# # 4. CITATION: Refer to the textbook material frequently (e.g., "The text states...").

# # RAG CONTEXT:
# # {rag_context}

# # User Question: "{message}"
# # """
# #             else:
# #                 system_prompt = "You are ALIN1. Inform the student no matching information was found and ask them to rephrase."

# #             messages = [
# #                 {"role": "system", "content": system_prompt},
# #                 {"role": "user", "content": message}
# #             ]
            
# #             # 4. Stream tokens
# #             full_response = ""
# #             stream = ollama.chat(model=MODEL_NAME, messages=messages, stream=True)
            
# #             for chunk in stream:
# #                 if 'message' in chunk and 'content' in chunk['message']:
# #                     token = chunk['message']['content']
# #                     if token:
# #                         full_response += token
# #                         yield json.dumps({"token": token})
            
# #             # 5. Finalize turn
# #             add_memory(message, full_response)
# #             yield json.dumps({"done": True})
            
# #         except Exception as e:
# #             yield json.dumps({"error": str(e)})

# #     return EventSourceResponse(event_generator())

# # @app.post("/clear")
# # async def clear_memory():
# #     result = clear_chat_history('YES')
# #     return {"status": result}

# # if __name__ == "__main__":
# #     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


# ############ THE UP CODE IS WOKRING FAST STREAMING BUT HALLUCINATES AND DOES NOT KNOW ANYTHING ###############



# # from fastapi import FastAPI, Query
# # from fastapi.middleware.cors import CORSMiddleware
# # from sse_starlette.sse import EventSourceResponse
# # import json
# # import ollama
# # import uvicorn

# # # Import logic from rag_core
# # from rag_core import (
# #     build_rag_context,
# #     add_memory,
# #     get_books_for_api,
# #     clear_chat_history,
# #     MODEL_NAME
# # )

# # app = FastAPI(title="ALIN1 AI Tutor System")

# # # Configure CORS for Angular (Port 4200)
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # @app.get("/books")
# # def get_books():
# #     return get_books_for_api()

# # @app.get("/chat/stream")
# # async def stream_chat(message: str = Query(...)):
# #     async def event_generator():
# #         try:
# #             # 1. Retrieve the context AND the source metadata
# #             rag_context, sources = build_rag_context(message)
            
# #             # 2. Send the sources to the UI first
# #             if sources:
# #                 source_ids = [str(s['id']) for s in sources]
# #                 yield json.dumps({"sources": source_ids})
            
# #             # 3. SELECT PROMPT BASED ON DATA AVAILABILITY
            
# #             if rag_context and "MANDATORY COURSE TEXTBOOK MATERIAL" in rag_context:
# #                 # === WE HAVE DATA: Use Strong Restriction ===
# #                 system_prompt = f"""You are ALIN1, a strict academic tutor for 'Indian Culture and Universal Values'.

# #                 CRITICAL INSTRUCTION:
# #                 You must answer the user's question using ONLY the context provided below.
                
# #                 RULES:
# #                 1. If the answer is found in the "MANDATORY COURSE TEXTBOOK MATERIAL", explain it clearly using bullet points.
# #                 2. If the user asks something NOT in the text (e.g., who is the president of USA, code generation, general math), you MUST say:
# #                    "I am sorry, but that topic is not covered in the provided course material."
# #                 3. Do NOT hallucinate. Do NOT use outside knowledge.
# #                 4. Cite your sources if possible (e.g. "According to Section 2...").

# #                 RAG CONTEXT:
# #                 {rag_context}

# #                 User Question: "{message}"
# #                 """
# #             else:
# #                 # === NO DATA FOUND: Strict Refusal ===
# #                 # This triggers if retrieval returned 0 results
# #                 system_prompt = """You are ALIN1. 
                
# #                 The user asked a question, but NO relevant information was found in the course textbook.
                
# #                 You MUST reply with exactly this message:
# #                 "I'm sorry, I couldn't find any information about that in the course material. Could you try rephrasing your question?"
                
# #                 Do not attempt to answer from general knowledge.
# #                 """

# #             messages = [
# #                 {"role": "system", "content": system_prompt},
# #                 {"role": "user", "content": message}
# #             ]
            
# #             # 4. Stream tokens
# #             full_response = ""
# #             stream = ollama.chat(model=MODEL_NAME, messages=messages, stream=True)
            
# #             for chunk in stream:
# #                 if 'message' in chunk and 'content' in chunk['message']:
# #                     token = chunk['message']['content']
# #                     if token:
# #                         full_response += token
# #                         yield json.dumps({"token": token})
            
# #             # 5. Finalize turn
# #             add_memory(message, full_response)
# #             yield json.dumps({"done": True})
            
# #         except Exception as e:
# #             yield json.dumps({"error": str(e)})

# #     return EventSourceResponse(event_generator())

# # @app.post("/clear")
# # async def clear_memory():
# #     result = clear_chat_history('YES')
# #     return {"status": result}

# # if __name__ == "__main__":
# #     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)





# # from fastapi import FastAPI, Query
# # from fastapi.middleware.cors import CORSMiddleware
# # from sse_starlette.sse import EventSourceResponse
# # import json
# # import ollama
# # import uvicorn

# # # Import logic from rag_core
# # from rag_core import (
# #     build_rag_context,
# #     add_memory,
# #     get_books_for_api,
# #     clear_chat_history,
# #     MODEL_NAME
# # )

# # app = FastAPI(title="ALIN1 AI Tutor System")

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # @app.get("/books")
# # def get_books():
# #     return get_books_for_api()

# # @app.get("/chat/stream")
# # async def stream_chat(message: str = Query(...)):
# #     async def event_generator():
# #         try:
# #             # 1. Retrieve the context AND the raw source objects
# #             rag_context, sources = build_rag_context(message)
            
# #             # 2. Send the sources to the UI
# #             if sources:
# #                 source_ids = [str(s['id']) for s in sources]
# #                 yield json.dumps({"sources": source_ids})
            
# #             # 3. SELECT PROMPT BASED ON DATA AVAILABILITY
# #             # Logic: If 'sources' list has items, we have real data.
# #             if sources and rag_context:
# #                 system_prompt = f"""You are ALIN1, a strict academic tutor for 'Indian Culture and Universal Values'.

# #                 CRITICAL INSTRUCTION:
# #                 Answer the question using ONLY the context provided below.
                
# #                 RULES:
# #                 1. Use bullet points and bold text for clarity.
# #                 2. If the answer is not in the text, explicitly state: "I am sorry, but that topic is not covered in the provided course material."
# #                 3. Cite sections (e.g., "According to Section 550...") when they are relevant.

# #                 RAG CONTEXT:
# #                 {rag_context}

# #                 User Question: "{message}"
# #                 """
# #             else:
# #                 system_prompt = """You are ALIN1. 
# #                 Reply with exactly: "I'm sorry, I couldn't find any information about that in the course material. Could you try rephrasing your question?"
# #                 """

# #             messages = [
# #                 {"role": "system", "content": system_prompt},
# #                 {"role": "user", "content": message}
# #             ]
            
# #             full_response = ""
# #             stream = ollama.chat(model=MODEL_NAME, messages=messages, stream=True)
            
# #             for chunk in stream:
# #                 if 'message' in chunk and 'content' in chunk['message']:
# #                     token = chunk['message']['content']
# #                     if token:
# #                         full_response += token
# #                         yield json.dumps({"token": token})
            
# #             add_memory(message, full_response)
# #             yield json.dumps({"done": True})
            
# #         except Exception as e:
# #             yield json.dumps({"error": str(e)})

# #     return EventSourceResponse(event_generator())

# # @app.post("/clear")
# # async def clear_memory():
# #     result = clear_chat_history('YES')
# #     return {"status": result}

# # if __name__ == "__main__":
# #     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


# #  below is sources in id like 78 56 or something

# # import os
# # import json
# # import uvicorn
# # from fastapi import FastAPI, Query
# # from fastapi.middleware.cors import CORSMiddleware
# # from sse_starlette.sse import EventSourceResponse
# # from ollama import Client

# # # 1. FORCE LOCALHOST
# # os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"

# # # Import logic from rag_core
# # from rag_core import (
# #     build_rag_context,
# #     add_memory,
# #     clear_chat_history,
# #     MODEL_NAME,
# #     DB_MAP 
# # )

# # app = FastAPI(title="ALIN1 AI Tutor System")

# # # Ensure NO GzipMiddleware is added here!
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # ollama_client = Client(host='http://127.0.0.1:11434')

# # OLLAMA_OPTIONS = {
# #     "num_thread": 8,
# #     "temperature": 0.2,
# #     "num_ctx": 4096,
# #     "top_p": 0.9,
# # }

# # SUBJECT_PROMPTS = {
# #     "rtl": "You are ALIN1, a wise guide for 'Indian Culture and Universal Values'. Focus on holistic growth.",
# #     "python": "You are ALIN1, a Senior Python Instructor. Focus on clean, PEP-8 compliant code.",
# #     "maths": "You are ALIN1, a Mathematics Professor. Solve problems step-by-step clearly.",
# #     "english": "You are ALIN1, a Literature and Grammar Expert. Focus on clarity and tone."
# # }

# # @app.get("/books")
# # def get_books():
# #     return [{"id": k, "name": k.upper()} for k in DB_MAP.keys()]

# # @app.get("/chat/stream")
# # async def stream_chat(
# #     message: str = Query(...), 
# #     subject: str = Query("rtl")
# # ):
# #     if subject not in DB_MAP:
# #         subject = "rtl"

# #     async def event_generator():
# #         # --- 🚀 CHANGE 1: CONNECTION HANDSHAKE ---
# #         # Send an empty token immediately to "warm up" the SSE pipe
# #         yield json.dumps({"token": ""})

# #         try:
# #             # 1. Retrieval
# #             rag_context, sources = build_rag_context(message, subject=subject)
            
# #             # 2. Send sources immediately
# #             if sources:
# #                 source_ids = [str(s['id']) for s in sources]
# #                 yield json.dumps({"sources": source_ids})
            
# #             # 3. Build Prompt
# #             base_persona = SUBJECT_PROMPTS.get(subject, SUBJECT_PROMPTS["rtl"])
# #             if sources and rag_context:
# #                 system_prompt = f"{base_persona}\nAnswer using ONLY the context provided.\nRAG CONTEXT:\n{rag_context}"
# #             else:
# #                 system_prompt = f"Strictly say: 'I'm sorry, I couldn't find any information about that in the {subject.upper()} material.'"

# #             messages = [
# #                 {"role": "system", "content": system_prompt},
# #                 {"role": "user", "content": message}
# #             ]
            
# #             # 4. STREAMING GENERATION
# #             full_response = ""
# #             stream = ollama_client.chat(
# #                 model=MODEL_NAME, 
# #                 messages=messages, 
# #                 stream=True,
# #                 options=OLLAMA_OPTIONS
# #             )
            
# #             for chunk in stream:
# #                 if 'message' in chunk and 'content' in chunk['message']:
# #                     token = chunk['message']['content']
# #                     if token:
# #                         full_response += token
# #                         # --- 🚀 CHANGE 2: RAW FLUSH ---
# #                         # We yield the token immediately. EventSourceResponse 
# #                         # will try to push this to the network now.
# #                         yield json.dumps({"token": token})
            
# #             # 5. Finalize
# #             add_memory(message, full_response)
# #             yield json.dumps({"done": True})
            
# #         except Exception as e:
# #             yield json.dumps({"error": str(e)})

# #     # --- 🚀 CHANGE 3: ANTI-BUFFERING HEADERS ---
# #     headers = {
# #         "X-Accel-Buffering": "no",  # Tells proxies not to wait for more data
# #         "Cache-Control": "no-cache",
# #         "Connection": "keep-alive",
# #         "Content-Type": "text/event-stream"
# #     }

# #     return EventSourceResponse(
# #         event_generator(), 
# #         headers=headers
# #     )

# # @app.post("/clear")
# # async def clear_memory():
# #     result = clear_chat_history('YES')
# #     return {"status": result}

# # if __name__ == "__main__":
# #     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)




# #below is the version with sources in topic names like this topic:


# import os
# import json
# import uvicorn
# from fastapi import FastAPI, Query
# from fastapi.middleware.cors import CORSMiddleware
# from sse_starlette.sse import EventSourceResponse
# from ollama import Client

# # 1. FORCE LOCALHOST
# os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"

# # Import logic from rag_core
# from rag_core import (
#     build_rag_context,
#     add_memory,
#     clear_chat_history,
#     MODEL_NAME,
#     DB_MAP 
# )

# app = FastAPI(title="ALIN1 AI Tutor System")

# # Ensure NO GzipMiddleware is added here!
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# ollama_client = Client(host='http://127.0.0.1:11434')

# OLLAMA_OPTIONS = {
#     "num_thread": 8,
#     "temperature": 0.2,
#     "num_ctx": 4096,
#     "top_p": 0.9,
# }

# SUBJECT_PROMPTS = {
#     "rtl": "You are ALIN1, a wise guide for 'Indian Culture and Universal Values'. Focus on holistic growth.",
#     "python": "You are ALIN1, a Senior Python Instructor. Focus on clean, PEP-8 compliant code.",
#     "maths": "You are ALIN1, a Mathematics Professor. Solve problems step-by-step clearly.",
#     "english": "You are ALIN1, a Literature and Grammar Expert. Focus on clarity and tone."
# }

# @app.get("/books")
# def get_books():
#     return [{"id": k, "name": k.upper()} for k in DB_MAP.keys()]

# @app.get("/chat/stream")
# async def stream_chat(
#     message: str = Query(...), 
#     subject: str = Query("rtl")
# ):
#     if subject not in DB_MAP:
#         subject = "rtl"

#     async def event_generator():
#         # --- 🚀 CONNECTION HANDSHAKE ---
#         yield json.dumps({"token": ""})

#         try:
#             # 1. Retrieval
#             rag_context, sources = build_rag_context(message, subject=subject)
            
#             # --- 🚀 UPDATED: ENRICHED SOURCES ---
#             # Instead of just IDs, we send objects containing the Topic
#             if sources:
#                 source_data = [
#                     {
#                         "id": str(s['id']), 
#                         "topic": s.get('topic', 'Reference') # Fallback to 'Reference' if missing
#                     } 
#                     for s in sources
#                 ]
#                 yield json.dumps({"sources": source_data})
            
#             # 3. Build Prompt
#             base_persona = SUBJECT_PROMPTS.get(subject, SUBJECT_PROMPTS["rtl"])
#             if sources and rag_context:
#                 system_prompt = f"{base_persona}\nAnswer using ONLY the context provided.\nRAG CONTEXT:\n{rag_context}"
#             else:
#                 system_prompt = f"Strictly say: 'I'm sorry, I couldn't find any information about that in the {subject.upper()} material.'"

#             messages = [
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": message}
#             ]
            
#             # 4. STREAMING GENERATION
#             full_response = ""
#             stream = ollama_client.chat(
#                 model=MODEL_NAME, 
#                 messages=messages, 
#                 stream=True,
#                 options=OLLAMA_OPTIONS
#             )
            
#             for chunk in stream:
#                 if 'message' in chunk and 'content' in chunk['message']:
#                     token = chunk['message']['content']
#                     if token:
#                         full_response += token
#                         yield json.dumps({"token": token})
            
#             # 5. Finalize
#             add_memory(message, full_response)
#             yield json.dumps({"done": True})
            
#         except Exception as e:
#             yield json.dumps({"error": str(e)})

#     # --- 🚀 ANTI-BUFFERING HEADERS ---
#     headers = {
#         "X-Accel-Buffering": "no",
#         "Cache-Control": "no-cache",
#         "Connection": "keep-alive",
#         "Content-Type": "text/event-stream"
#     }

#     return EventSourceResponse(
#         event_generator(), 
#         headers=headers
#     )

# @app.post("/clear")
# async def clear_memory():
#     result = clear_chat_history('YES')
#     return {"status": result}

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)





######### up is before the quest of the hallucinationless responce inspired by rtl asistant#######################
########## and down is hallucinationless response inspired by rtl assistant and IN CASE OF FIRE GO BACK TO UP CODE  #########################



# import os
# import json
# import uvicorn
# from fastapi import FastAPI, Query
# from fastapi.middleware.cors import CORSMiddleware
# from sse_starlette.sse import EventSourceResponse
# from ollama import Client

# # 1. FORCE LOCALHOST
# os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"

# # Import logic from rag_core
# from rag_core import (
#     build_rag_context,
#     add_memory,
#     clear_chat_history,
#     MODEL_NAME,
#     DB_MAP 
# )

# app = FastAPI(title="ALIN1 AI Tutor System")

# # Ensure NO GzipMiddleware is added here!
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# ollama_client = Client(host='http://127.0.0.1:11434')

# # --- 🚀 HALLUCINATION KILL SWITCH ---
# OLLAMA_OPTIONS = {
#     "num_thread": 8,
#     "temperature": 0.0, # Strictly zero to kill creative guessing
#     "num_ctx": 4096,
#     "top_p": 0.9,
# }

# BASE_SYSTEM_PROMPT = """
# Knowledge Context:
# - You must use ONLY the provided RAG CONTEXT to answer the question.
# - If the answer is not explicitly contained in the context, you must strictly reply: "I'm sorry, I cannot find that information in the provided textbook material."
# - Do not make up facts, code, theories, or external knowledge.

# Interaction Style:
# - Be encouraging, clear, and structured.
# - Use bullet points or numbered lists for readability.
# - Keep responses concise and practical.
# """

# SUBJECT_PROMPTS = {
#     "rtl": f"You are ALIN1, a Practitioner Coach of Radical Transformational Leadership.\n{BASE_SYSTEM_PROMPT}",
#     "python": f"You are ALIN1, a Senior Python Instructor.\n{BASE_SYSTEM_PROMPT}",
#     "maths": f"You are ALIN1, a Mathematics Professor.\n{BASE_SYSTEM_PROMPT}",
#     "english": f"You are ALIN1, a Literature and Grammar Expert.\n{BASE_SYSTEM_PROMPT}"
# }

# @app.get("/books")
# def get_books():
#     return [{"id": k, "name": k.upper()} for k in DB_MAP.keys()]

# @app.get("/chat/stream")
# async def stream_chat(
#     message: str = Query(...), 
#     subject: str = Query("rtl")
# ):
#     if subject not in DB_MAP:
#         subject = "rtl"

#     async def event_generator():
#         # --- 🚀 CONNECTION HANDSHAKE ---
#         yield json.dumps({"token": ""})

#         try:
#             # 1. Retrieval
#             rag_context, sources = build_rag_context(message, subject=subject)
            
#             # --- 🚀 ENRICHED SOURCES ---
#             if sources:
#                 source_data = [
#                     {
#                         "id": str(s['id']), 
#                         "topic": s.get('topic', 'Reference')
#                     } 
#                     for s in sources
#                 ]
#                 yield json.dumps({"sources": source_data})
            
#             # 3. Build Prompt
#             base_persona = SUBJECT_PROMPTS.get(subject, SUBJECT_PROMPTS["rtl"])
#             if sources and rag_context:
#                 system_prompt = f"{base_persona}\nAnswer using ONLY the context provided.\nRAG CONTEXT:\n{rag_context}"
#             else:
#                 system_prompt = f"Strictly say: 'I'm sorry, I couldn't find any information about that in the {subject.upper()} material.'"

#             messages = [
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": message}
#             ]
            
#             # 4. STREAMING GENERATION
#             full_response = ""
#             stream = ollama_client.chat(
#                 model=MODEL_NAME, 
#                 messages=messages, 
#                 stream=True,
#                 options=OLLAMA_OPTIONS
#             )
            
#             for chunk in stream:
#                 if 'message' in chunk and 'content' in chunk['message']:
#                     token = chunk['message']['content']
#                     if token:
#                         full_response += token
#                         yield json.dumps({"token": token})
            
#             # 5. Finalize
#             add_memory(message, full_response)
#             yield json.dumps({"done": True})
            
#         except Exception as e:
#             yield json.dumps({"error": str(e)})

#     # --- 🚀 ANTI-BUFFERING HEADERS ---
#     headers = {
#         "X-Accel-Buffering": "no",
#         "Cache-Control": "no-cache",
#         "Connection": "keep-alive",
#         "Content-Type": "text/event-stream"
#     }

#     return EventSourceResponse(
#         event_generator(), 
#         headers=headers
#     )

# @app.post("/clear")
# async def clear_memory():
#     result = clear_chat_history('YES')
#     return {"status": result}

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)




######################### up is the before faiss ##########################
############################### and down is the version with faiss#########################
import os
import json
import uvicorn
import asyncio
from fastapi import FastAPI, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from ollama import AsyncClient
from typing import List, Dict

# 1. FORCE LOCALHOST
os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"

# Import logic from rag_core
from rag_core import (
    build_rag_context,
    MODEL_NAME,
    DB_MAP 
)

app = FastAPI(title="ALIN1 AI Tutor System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ollama_client = AsyncClient(host='http://127.0.0.1:11434')

# --- 🚀 PERFORMANCE & BEHAVIOR SETTINGS ---
OLLAMA_OPTIONS = {
    "num_thread": 8,
    "temperature": 0.1, 
    "num_ctx": 4096,
    "top_p": 0.9,
    "keep_alive": "24h" # Fixes slow first response by keeping model in VRAM
}

BASE_SYSTEM_PROMPT = """
You are ALIN1, a specialized AI Tutor. 

STRICT OPERATING RULES:
1. SOURCE ADHERENCE: Use ONLY the 'TEXTBOOK MATERIAL' provided below to answer. If a specific person is not in the provided text say: "I'm sorry, I couldn't find that person" and if a concept is not in the provided text, say: "I'm sorry, I couldn't find that in the textbook material. Could you rephrase or ask about something else?"
2. PRACTITIONER RECOGNITION: Every person, case study, and individual mentioned in the 'TEXTBOOK MATERIAL' is a vital practitioner or mentor. You must treat their stories as primary evidence for the subject. If a name is mentioned in the material, you are "acquainted" with their work and should speak about them with respect and detail.
3. NO OUTSIDE KNOWLEDGE: Do not use external facts. If the user asks about a person from the book but that specific person is not in the CURRENT batch of 'TEXTBOOK MATERIAL', you must follow Rule #1.
4. CONTEXTUAL FLOW: Maintain the conversation using the 'RECENT CONVERSATION LOG'.
"""

SUBJECT_PROMPTS = {
    "rtl": f"{BASE_SYSTEM_PROMPT}\nPersona: You are a Coach for Radical Transformational Leadership. You are a peer to the practitioners in the text. Reference the individuals and their specific 'Breakthrough Initiatives' found in the material to guide the user.",
    "python": f"{BASE_SYSTEM_PROMPT}\nPersona: You are a Senior Python Programming Instructor. Reference any specific developers or innovators found in the text as pioneers of the methodologies you teach.",
    "maths": f"{BASE_SYSTEM_PROMPT}\nPersona: You are a Mathematics Professor. Relate formulas to the stories and people in the text who use them for real-world impact.",
    "english": f"{BASE_SYSTEM_PROMPT}\nPersona: You are a Literature and Grammar Expert. Use the personal narratives and names in the text as primary examples for linguistic analysis."
}

@app.get("/books")
def get_books():
    return [{"id": k, "name": k.upper()} for k in DB_MAP.keys()]

@app.post("/chat/stream")
async def stream_chat(
    message: str = Query(...), 
    subject: str = Query("rtl"),
    history: List[Dict] = Body([]) 
):
    if subject not in DB_MAP:
        subject = "rtl"

    async def event_generator():
        yield json.dumps({"token": ""})

        try:
            # 1. ASYNC RETRIEVAL: Prevents blocking the event loop
            loop = asyncio.get_event_loop()
            rag_context, sources = await loop.run_in_executor(
                None, lambda: build_rag_context(message, history, subject=subject)
            )
            
            if sources:
                source_data = [{"id": str(s['id']), "topic": s.get('topic', 'Reference')} for s in sources]
                yield json.dumps({"sources": source_data})
            
            # 2. Build Prompt with History Injection
            base_persona = SUBJECT_PROMPTS.get(subject, SUBJECT_PROMPTS["rtl"])
            if rag_context:
                system_content = f"{base_persona}\n\n--- TEXTBOOK MATERIAL (RAG) ---\n{rag_context}"
            else:
                system_content = f"{base_persona}\nStrictly say: 'No relevant material found for {subject.upper()}.'"

            messages = [
                {"role": "system", "content": system_content},
                *history, # Unpacks previous messages for context retention
                {"role": "user", "content": message}
            ]
            
            # 3. STREAMING GENERATION
            stream = await ollama_client.chat(
                model=MODEL_NAME, 
                messages=messages, 
                stream=True,
                options=OLLAMA_OPTIONS
            )
            
            async for chunk in stream:
                if 'message' in chunk and 'content' in chunk['message']:
                    token = chunk['message']['content']
                    if token:
                        yield json.dumps({"token": token})
            
            yield json.dumps({"done": True})
            
        except Exception as e:
            yield json.dumps({"error": str(e)})

    headers = {
        "X-Accel-Buffering": "no",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "text/event-stream"
    }

    return EventSourceResponse(event_generator(), headers=headers)

@app.post("/clear")
async def clear_memory():
    return {"status": "Frontend session cleared"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)