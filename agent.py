import json, os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import uvicorn

# Load brain
brain = ""
brain_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brain.json")
with open(brain_path, "r", encoding="utf-8") as f:
    data = json.load(f)
if isinstance(data, list):
    for item in data:
        if isinstance(item, dict):
            brain += item.get("content", "")
        else:
            brain += str(item)
brain = brain[:12000]

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
SYSTEM_PROMPT = "You are Weberdy, sovereign AI of ForeFathers DAO.\n" + brain

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Message(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
def root():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "weberdy.html")) as f:
        return f.read()

@app.post("/chat")
def chat(msg: Message):
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": msg.message}
        ]
    }
    r = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
    return {"response": r.json()["choices"][0]["message"]["content"]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
