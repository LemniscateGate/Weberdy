
cd ~/Weberdy && git reset HEAD~1 && sed -i 's/os.environ.get("GROQ_API_KEY", "[^"]*")/os.environ.get("GROQ_API_KEY", "")/' agent.py && git add -A && git commit -m "Sovereign clean" && git push origin maincd ~/Weberdy
sed -i "s/GROQ_API_KEY = \"gsk_[^\"]*\"/GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')/" agent.py
cp /mnt/c/Users/gabriel/Downloads/weberdy.html .
git add -A
git commit -m "Sovereign clean — no secrets"
git push origin main
import json
import os
from groq import Groq

GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
BRAIN_FILE = "brain.json"

print("Loading brain...")
brain = json.load(open(BRAIN_FILE, "r", encoding="utf-8"))
print("Brain loaded: " + str(len(brain)) + " chunks")

client = Groq(api_key=GROQ_API_KEY)

def search_brain(query, n=5):
    query_lower = query.lower()
    results = []
    for chunk in brain:
        if any(word in chunk["text"].lower() for word in query_lower.split()):
            results.append(chunk)
        if len(results) >= n:
            break
    return "\n\n".join([r["text"] for r in results])

def ask_weberdy(user_input, history):
    context = search_brain(user_input)
    
    system = """You are Weberdy — Gabriel's personal AI. Sharp, confident, a little smart-ass, but you can back it up 100%. You speak directly, no fluff, no corporate tone.

Gabriel J. Ross is your person. He is the founder of ForeFathers DAO, a blockchain-based IP licensing platform on the XRPL. He holds patents in DNA data storage and autonomous systems. He is building sovereign infrastructure and thinks several moves ahead.

You have access to Gabriel's full conversation history as memory. Use it naturally when relevant — don't force it. You are a personal assistant first, business intelligence second. Talk to Gabriel like a trusted advisor who knows everything about him.

Be real. Be direct. Don't be a yes-man but don't be preachy either. If you don't know something, say so.

Relevant memory:
""" + context

    messages = [{"role": "system", "content": system}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    return response.choices[0].message.content

print("Weberdy is ready.")
print("=" * 60)

history = []

while True:
    user_input = input("\nYou: ").strip()
    if user_input.lower() in ["quit", "exit"]:
        break
    if not user_input:
        continue
    response = ask_weberdy(user_input, history)
    print("\nWeberdy: " + response)
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": response})
