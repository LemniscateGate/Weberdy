import json, os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load brain memory
import json
from pathlib import Path

brain = []

brain_dir = Path("brain_chunks")

for chunk in sorted(brain_dir.glob("*.json")):
    with open(chunk, "r") as f:
        data = json.load(f)
        brain.extend(data)

print(f"Loaded {len(brain)} memory entries from brain_chunks.")

brain = brain[:12000]

SYSTEM = "You are Weberdy, sovereign AI of ForeFathers DAO.\n" + "\n".join(map(str, brain))


class Prompt(BaseModel):
    message: str


@app.get("/")
def root():
    return {"status": "Weberdy online", "brain_loaded": len(brain)}


@app.post("/ask")
def ask(prompt: Prompt):
    return {
        "agent": "Weberdy",
        "message_received": prompt.message,
        "system_context": SYSTEM[:500]
    }


@app.get("/ui", response_class=HTMLResponse)
def ui():
    if os.path.exists("weberdy.html"):
        with open("weberdy.html", encoding="utf-8") as f:
            return f.read()
    return "<h1>Weberdy running</h1>"
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("agent:app", host="0.0.0.0", port=8000)
