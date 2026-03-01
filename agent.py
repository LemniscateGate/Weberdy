import json, os, glob
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import uvicorn

brain = ""
chunk_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brain_chunks")
chunk_files = sorted(glob.glob(os.path.join(chunk_dir, "*.json")))
for chunk_file in chunk_files:
    with open(chunk_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        if isinstance(item, dict):
            brain += item.get("text", "") + " "
brain = brain[:12000]

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
ELEVEN_API_KEY = os.environ.get("ELEVEN_API_KEY", "")
ELEVEN_VOICE_ID = os.environ.get("ELEVEN_VOICE_ID", "jqcCZkN6Knx8BJ5TBdYR")
SYSTEM_PROMPT = "You are Weberdy, sovereign AI of ForeFathers DAO.\n" + brain

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Message(BaseModel):
    message: str

class TTSRequest(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
def root():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "weberdy.html")) as f:
        return f.read()

@app.post("/chat")
def chat(msg: Message):
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": msg.message}]}
    r = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
    return {"response": r.json()["choices"][0]["message"]["content"]}

@app.post("/tts")
def tts(req: TTSRequest):
    headers = {"xi-api-key": ELEVEN_API_KEY, "Content-Type": "application/json"}
    payload = {"text": req.text, "model_id": "eleven_monolingual_v1", "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}}
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_VOICE_ID}", json=payload, headers=headers, stream=True)
    return StreamingResponse(r.iter_content(chunk_size=1024), media_type="audio/mpeg")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
