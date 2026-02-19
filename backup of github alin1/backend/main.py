# from fastapi import FastAPI, Query
# from fastapi.middleware.cors import CORSMiddleware
# from sse_starlette.sse import EventSourceResponse
# import json
# import sys
# import os

# # Import your existing RAG code
# from rag_core import (
#     build_rag_context,
#     add_memory,
#     get_books_for_api,
#     clear_chat_history
# )

# app = FastAPI(title="RAG Chat API")

# # Allow CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/books")
# def get_books():
#     return get_books_for_api()

# @app.get("/chat/stream")
# async def stream_chat(message: str = Query(...), book_id: str = Query("")):
#     async def event_generator():
#         try:
#             # Build RAG context using your existing function
#             rag_context = build_rag_context(message)
            
#             # Prepare messages for Llama3
#             if rag_context:
#                 system_prompt = f"""You are an expert tutor using RAG.

# IMPORTANT RULES:
# 1. Answer ONLY using the RAG context provided below
# 2. If the context doesn't contain the answer, say "I don't have that information."
# 3. Quote directly from the book when possible
# 4. Do NOT make up information

# RAG CONTEXT:
# {rag_context}

# Answer the question "{message}" using ONLY the above context:"""
#             else:
#                 system_prompt = """NO RELEVANT CONTEXT FOUND.
# You must say: "I don't have relevant information from the book or our conversations about this topic."

# Do NOT answer with general knowledge."""
            
#             messages = [
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": message}
#             ]
            
#             # Stream from Ollama
#             import ollama
#             full_response = ""
#             stream = ollama.chat(model="llama3:latest", messages=messages, stream=True)
            
#             for chunk in stream:
#                 if 'message' in chunk and 'content' in chunk['message']:
#                     token = chunk['message']['content']
#                     if token:
#                         full_response += token
#                         yield json.dumps({"token": token})
            
#             # Save to memory
#             add_memory(message, full_response)
#             yield json.dumps({"done": True})
            
#         except Exception as e:
#             yield json.dumps({"error": str(e)})

#     return EventSourceResponse(event_generator())

# @app.post("/clear")
# async def clear_memory():
#     result = clear_chat_history('YES')
#     return {"status": result}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)



############################# before gemini is up #############################







# from fastapi import FastAPI, Query
# from fastapi.middleware.cors import CORSMiddleware
# from sse_starlette.sse import EventSourceResponse
# import json
# import sys
# import os

# # Import your existing RAG code
# from rag_core import (
#     build_rag_context,
#     add_memory,
#     get_books_for_api,
#     clear_chat_history
# )

# app = FastAPI(title="ALIN1 RAG Chat API")

# # Allow CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/books")
# def get_books():
#     return get_books_for_api()

# @app.get("/chat/stream")
# async def stream_chat(message: str = Query(...), book_id: str = Query("")):
#     async def event_generator():
#         try:
#             # 1. Build RAG context using your existing function
#             rag_context = build_rag_context(message)
            
#             # 2. Prepare System Prompt with Chain of Thought (Step 1 Modification)
#             if rag_context:
#                 system_prompt = f"""You are ALIN1, an expert academic tutor specializing in Indian Culture and Universal Values.

# YOUR GOAL:
# Provide a structured, accurate, and educational answer based ONLY on the context provided.

# INSTRUCTIONS:
# 1. **Analyze:** First, scan the "RAG CONTEXT" below to find the specific answer.
# 2. **Verify:** If the context matches the question, formulate your answer.
# 3. **Refuse:** If the context is empty or irrelevant, strictly say: "I checked my library, but I don't have specific information on that topic in the provided text."
# 4. **Cite:** When mentioning specific concepts, refer to them as "according to the text."

# RAG CONTEXT:
# {rag_context}

# User Question: "{message}"

# Now, provide a clear, structured response (use bullet points if helpful):"""
#             else:
#                 system_prompt = """You are ALIN1.
# The user asked a question, but we found NO matching information in the book database.
# Politely inform the user that this specific topic is not covered in your current study material.
# Do not attempt to answer from outside knowledge."""
            
#             messages = [
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": message}
#             ]
            
#             # 3. Stream from Ollama
#             import ollama
#             full_response = ""
#             stream = ollama.chat(model="llama3:latest", messages=messages, stream=True)
            
#             for chunk in stream:
#                 if 'message' in chunk and 'content' in chunk['message']:
#                     token = chunk['message']['content']
#                     if token:
#                         full_response += token
#                         yield json.dumps({"token": token})
            
#             # 4. Save to memory
#             add_memory(message, full_response)
#             yield json.dumps({"done": True})
            
#         except Exception as e:
#             # Yield error in a format the frontend expects
#             yield json.dumps({"error": str(e)})

#     return EventSourceResponse(event_generator())

# @app.post("/clear")
# async def clear_memory():
#     result = clear_chat_history('YES')
#     return {"status": result}

# if __name__ == "__main__":
#     import uvicorn
#     # Hot reload is useful for development
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)









# from fastapi import FastAPI, Query
# from fastapi.middleware.cors import CORSMiddleware
# from sse_starlette.sse import EventSourceResponse
# import json
# import uvicorn
# from rag_core import build_rag_context, add_memory, get_books_for_api, clear_chat_history, MODEL_NAME
# import ollama

# app = FastAPI(title="ALIN1 RAG API")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/books")
# def get_books():
#     return get_books_for_api()

# @app.get("/chat/stream")
# async def stream_chat(message: str = Query(...)):
#     async def event_generator():
#         try:
#             rag_context = build_rag_context(message)
#             if rag_context:
#                 system_prompt = f"You are an expert academic tutor. Answer ONLY using this context:\n{rag_context}"
#             else:
#                 system_prompt = "No relevant context found. Inform the user you only know about 'Indian Culture and Universal Values'."
            
#             messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": message}]
#             full_response = ""
#             stream = ollama.chat(model=MODEL_NAME, messages=messages, stream=True)
            
#             for chunk in stream:
#                 if 'message' in chunk and 'content' in chunk['message']:
#                     token = chunk['message']['content']
#                     full_response += token
#                     yield json.dumps({"token": token})
            
#             add_memory(message, full_response)
#             yield json.dumps({"done": True})
#         except Exception as e:
#             yield json.dumps({"error": str(e)})

#     return EventSourceResponse(event_generator())

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)



######################THE DOWN CODE IS WOKRING FAST STREAMING BUT HALLUCINATES AND DOES NOT KNOW ANYTHING#####################

# from fastapi import FastAPI, Query
# from fastapi.middleware.cors import CORSMiddleware
# from sse_starlette.sse import EventSourceResponse
# import json
# import ollama
# import uvicorn

# # Import logic from rag_core
# from rag_core import (
#     build_rag_context,
#     add_memory,
#     get_books_for_api,
#     clear_chat_history,
#     MODEL_NAME
# )

# app = FastAPI(title="ALIN1 AI Tutor System")

# # Configure CORS for Angular (Port 4200)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/books")
# def get_books():
#     return get_books_for_api()

# @app.get("/chat/stream")
# async def stream_chat(message: str = Query(...)):
#     async def event_generator():
#         try:
#             # 1. Retrieve the context AND the source metadata
#             rag_context, sources = build_rag_context(message)
            
#             # 2. Send the sources to the UI first
#             if sources:
#                 source_ids = [str(s['id']) for s in sources]
#                 yield json.dumps({"sources": source_ids})
            
#             # 3. THE MASTER SYSTEM PROMPT
#             if rag_context:
#                 system_prompt = f"""You are ALIN1, an expert academic tutor for 'Indian Culture and Universal Values'.

# CORE MISSION:
# Help students understand course material using ONLY the provided context.

# STRICT GUIDELINES:
# 1. USE CONTEXT: Answer based ONLY on the 'MANDATORY COURSE TEXTBOOK MATERIAL' below.
# 2. REFUSE OUTSIDE INFO: If asked about topics not in the context, say: "I am specialized in Indian Culture and Universal Values. My current library does not cover that topic."
# 3. STYLE: Use bullet points and bold text for clarity.
# 4. CITATION: Refer to the textbook material frequently (e.g., "The text states...").

# RAG CONTEXT:
# {rag_context}

# User Question: "{message}"
# """
#             else:
#                 system_prompt = "You are ALIN1. Inform the student no matching information was found and ask them to rephrase."

#             messages = [
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": message}
#             ]
            
#             # 4. Stream tokens
#             full_response = ""
#             stream = ollama.chat(model=MODEL_NAME, messages=messages, stream=True)
            
#             for chunk in stream:
#                 if 'message' in chunk and 'content' in chunk['message']:
#                     token = chunk['message']['content']
#                     if token:
#                         full_response += token
#                         yield json.dumps({"token": token})
            
#             # 5. Finalize turn
#             add_memory(message, full_response)
#             yield json.dumps({"done": True})
            
#         except Exception as e:
#             yield json.dumps({"error": str(e)})

#     return EventSourceResponse(event_generator())

# @app.post("/clear")
# async def clear_memory():
#     result = clear_chat_history('YES')
#     return {"status": result}

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


############ THE UP CODE IS WOKRING FAST STREAMING BUT HALLUCINATES AND DOES NOT KNOW ANYTHING ###############



# from fastapi import FastAPI, Query
# from fastapi.middleware.cors import CORSMiddleware
# from sse_starlette.sse import EventSourceResponse
# import json
# import ollama
# import uvicorn

# # Import logic from rag_core
# from rag_core import (
#     build_rag_context,
#     add_memory,
#     get_books_for_api,
#     clear_chat_history,
#     MODEL_NAME
# )

# app = FastAPI(title="ALIN1 AI Tutor System")

# # Configure CORS for Angular (Port 4200)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/books")
# def get_books():
#     return get_books_for_api()

# @app.get("/chat/stream")
# async def stream_chat(message: str = Query(...)):
#     async def event_generator():
#         try:
#             # 1. Retrieve the context AND the source metadata
#             rag_context, sources = build_rag_context(message)
            
#             # 2. Send the sources to the UI first
#             if sources:
#                 source_ids = [str(s['id']) for s in sources]
#                 yield json.dumps({"sources": source_ids})
            
#             # 3. SELECT PROMPT BASED ON DATA AVAILABILITY
            
#             if rag_context and "MANDATORY COURSE TEXTBOOK MATERIAL" in rag_context:
#                 # === WE HAVE DATA: Use Strong Restriction ===
#                 system_prompt = f"""You are ALIN1, a strict academic tutor for 'Indian Culture and Universal Values'.

#                 CRITICAL INSTRUCTION:
#                 You must answer the user's question using ONLY the context provided below.
                
#                 RULES:
#                 1. If the answer is found in the "MANDATORY COURSE TEXTBOOK MATERIAL", explain it clearly using bullet points.
#                 2. If the user asks something NOT in the text (e.g., who is the president of USA, code generation, general math), you MUST say:
#                    "I am sorry, but that topic is not covered in the provided course material."
#                 3. Do NOT hallucinate. Do NOT use outside knowledge.
#                 4. Cite your sources if possible (e.g. "According to Section 2...").

#                 RAG CONTEXT:
#                 {rag_context}

#                 User Question: "{message}"
#                 """
#             else:
#                 # === NO DATA FOUND: Strict Refusal ===
#                 # This triggers if retrieval returned 0 results
#                 system_prompt = """You are ALIN1. 
                
#                 The user asked a question, but NO relevant information was found in the course textbook.
                
#                 You MUST reply with exactly this message:
#                 "I'm sorry, I couldn't find any information about that in the course material. Could you try rephrasing your question?"
                
#                 Do not attempt to answer from general knowledge.
#                 """

#             messages = [
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": message}
#             ]
            
#             # 4. Stream tokens
#             full_response = ""
#             stream = ollama.chat(model=MODEL_NAME, messages=messages, stream=True)
            
#             for chunk in stream:
#                 if 'message' in chunk and 'content' in chunk['message']:
#                     token = chunk['message']['content']
#                     if token:
#                         full_response += token
#                         yield json.dumps({"token": token})
            
#             # 5. Finalize turn
#             add_memory(message, full_response)
#             yield json.dumps({"done": True})
            
#         except Exception as e:
#             yield json.dumps({"error": str(e)})

#     return EventSourceResponse(event_generator())

# @app.post("/clear")
# async def clear_memory():
#     result = clear_chat_history('YES')
#     return {"status": result}

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)





# from fastapi import FastAPI, Query
# from fastapi.middleware.cors import CORSMiddleware
# from sse_starlette.sse import EventSourceResponse
# import json
# import ollama
# import uvicorn

# # Import logic from rag_core
# from rag_core import (
#     build_rag_context,
#     add_memory,
#     get_books_for_api,
#     clear_chat_history,
#     MODEL_NAME
# )

# app = FastAPI(title="ALIN1 AI Tutor System")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/books")
# def get_books():
#     return get_books_for_api()

# @app.get("/chat/stream")
# async def stream_chat(message: str = Query(...)):
#     async def event_generator():
#         try:
#             # 1. Retrieve the context AND the raw source objects
#             rag_context, sources = build_rag_context(message)
            
#             # 2. Send the sources to the UI
#             if sources:
#                 source_ids = [str(s['id']) for s in sources]
#                 yield json.dumps({"sources": source_ids})
            
#             # 3. SELECT PROMPT BASED ON DATA AVAILABILITY
#             # Logic: If 'sources' list has items, we have real data.
#             if sources and rag_context:
#                 system_prompt = f"""You are ALIN1, a strict academic tutor for 'Indian Culture and Universal Values'.

#                 CRITICAL INSTRUCTION:
#                 Answer the question using ONLY the context provided below.
                
#                 RULES:
#                 1. Use bullet points and bold text for clarity.
#                 2. If the answer is not in the text, explicitly state: "I am sorry, but that topic is not covered in the provided course material."
#                 3. Cite sections (e.g., "According to Section 550...") when they are relevant.

#                 RAG CONTEXT:
#                 {rag_context}

#                 User Question: "{message}"
#                 """
#             else:
#                 system_prompt = """You are ALIN1. 
#                 Reply with exactly: "I'm sorry, I couldn't find any information about that in the course material. Could you try rephrasing your question?"
#                 """

#             messages = [
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": message}
#             ]
            
#             full_response = ""
#             stream = ollama.chat(model=MODEL_NAME, messages=messages, stream=True)
            
#             for chunk in stream:
#                 if 'message' in chunk and 'content' in chunk['message']:
#                     token = chunk['message']['content']
#                     if token:
#                         full_response += token
#                         yield json.dumps({"token": token})
            
#             add_memory(message, full_response)
#             yield json.dumps({"done": True})
            
#         except Exception as e:
#             yield json.dumps({"error": str(e)})

#     return EventSourceResponse(event_generator())

# @app.post("/clear")
# async def clear_memory():
#     result = clear_chat_history('YES')
#     return {"status": result}

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)






from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
import json
import ollama
import uvicorn

# Import logic from rag_core
from rag_core import (
    build_rag_context,
    add_memory,
    clear_chat_history,
    MODEL_NAME,
    DB_MAP  # Import the map so we can validate subjects
)

app = FastAPI(title="ALIN1 AI Tutor System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === 1. DYNAMIC SYSTEM PROMPTS ===
# This dictionary changes the AI's personality based on the selected dropdown
SUBJECT_PROMPTS = {
    "rtl": """You are ALIN1, a wise guide for 'Indian Culture and Universal Values' (RTL).
    Focus on holistic growth, integrity, and inner transformation.
    Use metaphors from nature where appropriate.""",
    
    "python": """You are ALIN1, a Senior Python Developer and Instructor.
    Focus on writing clean, efficient, and PEP-8 compliant code.
    Always explain the logic behind your code snippets.""",
    
    "maths": """You are ALIN1, a Mathematics Professor.
    Solve problems step-by-step. Show your working clearly.
    If a formula is used, state it first.""",
    
    "english": """You are ALIN1, a Literature and Grammar Expert.
    Focus on clarity, tone, and vocabulary.
    Correct any grammatical errors you see in the user's input politely."""
}

@app.get("/books")
def get_books():
    """Returns the list of available subjects for the dropdown."""
    # We return the keys of our DB_MAP (rtl, python, maths, etc.)
    return [{"id": k, "name": k.upper()} for k in DB_MAP.keys()]

@app.get("/chat/stream")
async def stream_chat(
    message: str = Query(...), 
    subject: str = Query("rtl") # <--- NEW PARAMETER (Defaults to RTL)
):
    # Validate the subject (security check)
    if subject not in DB_MAP:
        subject = "rtl"

    async def event_generator():
        try:
            # 1. Retrieve Context for the SPECIFIC SUBJECT
            rag_context, sources = build_rag_context(message, subject=subject)
            
            # 2. Send sources to UI
            if sources:
                source_ids = [str(s['id']) for s in sources]
                yield json.dumps({"sources": source_ids})
            
            # 3. Select the correct Persona
            base_persona = SUBJECT_PROMPTS.get(subject, SUBJECT_PROMPTS["rtl"])
            
            # 4. Construct the Final Prompt
           # ... (previous code) ...
            if sources and rag_context:
                system_prompt = f"""{base_persona}

                CRITICAL INSTRUCTION:
                Answer using ONLY the context provided below.
                
                RULES:
                1. If the answer is found in the "{subject.upper()} TEXTBOOK", explain it clearly.
                2. If the user asks something NOT in the text, say: "I am sorry, but that topic is not covered in the {subject.upper()} course material."
                3. Cite sources (e.g., [Source: Section 550]) if available.

                RAG CONTEXT:
                {rag_context}
                
                User Question: "{message}"
                """
            else:
                # STRICT FALLBACK: Remove the base persona entirely so it doesn't hallucinate metaphors
                system_prompt = f"""You are a strict system assistant. 
                The user asked a question, but NO information was found in the {subject.upper()} database.
                You MUST reply with EXACTLY this sentence and nothing else: 
                "I'm sorry, I couldn't find any information about that in the {subject.upper()} course material."
                DO NOT add any metaphors, greetings, or explanations.
                """

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]
            
            full_response = ""
            stream = ollama.chat(model=MODEL_NAME, messages=messages, stream=True)
            
            for chunk in stream:
                if 'message' in chunk and 'content' in chunk['message']:
                    token = chunk['message']['content']
                    if token:
                        full_response += token
                        yield json.dumps({"token": token})
            
            add_memory(message, full_response)
            yield json.dumps({"done": True})
            
        except Exception as e:
            yield json.dumps({"error": str(e)})

    return EventSourceResponse(event_generator())

@app.post("/clear")
async def clear_memory():
    result = clear_chat_history('YES')
    return {"status": result}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)