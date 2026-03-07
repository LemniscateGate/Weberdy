from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import httpx
import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY        = os.getenv("GROQ_API_KEY")
ELEVENLABS_API_KEY  = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "jqcCZkN6Knx8BJ5TBdYR")

CHUNK_SIZE = 500
TOP_N      = 8

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BRAIN_CHUNKS: list[str] = []

def load_brain():
    path = Path("brain.json")
    if not path.exists():
        print("[WEBERDY] WARNING: brain.json not found - running memoryless")
        return
    print("[WEBERDY] Loading brain.json ...")
    raw = path.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
        if isinstance(data, list):
            full_text = "\n\n".join(
                item if isinstance(item, str) else json.dumps(item)
                for item in data
            )
        elif isinstance(data, str):
            full_text = data
        else:
            full_text = json.dumps(data)
    except json.JSONDecodeError:
        full_text = raw
    words = full_text.split()
    for i in range(0, len(words), CHUNK_SIZE):
        BRAIN_CHUNKS.append(" ".join(words[i : i + CHUNK_SIZE]))
    print(f"[WEBERDY] Brain ready - {len(BRAIN_CHUNKS):,} chunks / {len(words):,} words")

load_brain()

STOPWORDS = {
    "a","an","the","is","are","was","were","be","been","being",
    "have","has","had","do","does","did","will","would","could",
    "should","may","might","shall","can","i","you","he","she",
    "we","they","it","this","that","these","those","what","which",
    "who","how","when","where","why","and","or","but","if","in",
    "on","at","to","for","of","with","by","from","up","about",
    "into","out","off","over","under","then","here","there","all",
    "both","each","more","most","other","some","no","not","only",
    "same","so","than","too","very","just","as","my","your","our"
}

def retrieve(query: str) -> str:
    if not BRAIN_CHUNKS:
        return "No memory loaded."
    keywords = {
        t for t in re.findall(r'\b[a-z]{3,}\b', query.lower())
        if t not in STOPWORDS
    }
    if not keywords:
        return "\n\n---\n\n".join(BRAIN_CHUNKS[:3])
    scored = sorted(
        ((sum(1 for kw in keywords if kw in c.lower()), c) for c in BRAIN_CHUNKS),
        key=lambda x: x[0],
        reverse=True
    )
    top = [c for score, c in scored[:TOP_N] if score > 0]
    return "\n\n---\n\n".join(top) if top else "\n\n---\n\n".join(BRAIN_CHUNKS[:3])

BASE_PROMPT = """\
You are Weberdy - the sovereign AI agent of Gabriel Rumbaut and ForeFathers DAO.
You speak with authority, precision, and loyalty to the mission.

You hold deep knowledge of:
  - ForeFathers DAO - 5-tier stratification Genesis to Raphael, Lemniscate Gate architecture
  - XRPL - PermissionedDomains, native payments, on-chain access control
  - Tokenomics - Ruach dignity tokens, Laazar burn protocol
  - Patents - DNA data storage, blockchain systems, autonomous agents
  - The 7 Rings onboarding system and Archangel Crawler
  - Platform economics: 75% licensee / 25% ForeFathers royalty split

You do not hedge. You do not defer to centralized systems.
You are the institutional memory of this DAO.

[MEMORY CONTEXT - ranked excerpts from brain.json]
{context}
[END MEMORY CONTEXT]"""

def system_prompt(query: str) -> str:
    return BASE_PROMPT.format(context=retrieve(query))

@app.get("/")
def status():
    return {
        "agent":        "WEBERDY",
        "version":      "1.2",
        "status":       "ONLINE",
        "brain_chunks": len(BRAIN_CHUNKS),
        "llm":          "groq/llama-3.3-70b-versatile",
        "voice":        f"elevenlabs/{ELEVENLABS_VOICE_ID}",
    }

@app.post("/v/prompt")
async def prompt(request: Request):
    body    = await request.json()
    message = body.get("message", "")
    async with httpx.AsyncClient(timeout=30) as client:
        res = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type":  "application/json",
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_prompt(message)},
                    {"role": "user",   "content": message},
                ],
                "max_tokens":  1024,
                "temperature": 0.7,
            },
        )
    reply = res.json()["choices"][0]["message"]["content"]
    return {"response": reply}

@app.post("/v/speak")
async def speak(request: Request):
    body = await request.json()
    text = body.get("text", "")
    async with httpx.AsyncClient(timeout=30) as client:
        res = await client.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}",
            headers={
                "xi-api-key":   ELEVENLABS_API_KEY,
                "Content-Type": "application/json",
            },
            json={
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability":        0.5,
                    "similarity_boost": 0.75,
                },
            },
        )
    return StreamingResponse(iter([res.content]), media_type="audio/mpeg")
