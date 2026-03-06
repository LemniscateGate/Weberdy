import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS so the IPFS interface can reach the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MEMORY_FILE = "brain.json"

class Prompt(BaseModel):
    message: str


def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


@app.post("/v/prompt")
async def prompt(p: Prompt):

    memory = load_memory()

    memory.append({
        "user": p.message
    })

    save_memory(memory)

    return {
        "response": "memory received",
        "message": p.message
    }


@app.get("/")
async def root():
    return {"status": "Weberdy API running"}
