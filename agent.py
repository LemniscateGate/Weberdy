import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MEMORY_FILE = "brain.json"

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

class Prompt(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"status": "Weberdy online"}

@app.post("/v/prompt")
async def prompt(p: Prompt):
    memory = load_memory()
    memory.append({"user": p.message})
    save_memory(memory)

    chat = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are Weberdy, sovereign AI of ForeFathers DAO. You assist Gabriel with XRPL, IP licensing, patents, and DAO governance."},
            {"role": "user", "content": p.message}
        ]
    )

    response = chat.choices[0].message.content

    return {
        "response": response,
        "message": p.message
    }
