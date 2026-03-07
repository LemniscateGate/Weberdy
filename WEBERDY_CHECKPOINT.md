WEBERDY SYSTEM CHECKPOINT
-------------------------

DATE: March 6, 2026

Current System State
====================

1. AI Agent Backend
-------------------

FastAPI agent running with Uvicorn.

Command used:

uvicorn agent:app --host 0.0.0.0 --port 8000

Status:
Server running successfully.


2. Agent Endpoint
-----------------

Endpoint:

POST /v1/prompt

Expected request format:

{
  "message": "Hello Weberdy"
}

Expected response format:

{
  "response": "..."
}


3. Frontend Chat Interface
--------------------------

Chat interface built with HTML + JavaScript.

Frontend sends requests using fetch():

http://127.0.0.1:8000/v1/prompt


Flow:

User input
↓
Frontend JS fetch()
↓
FastAPI endpoint
↓
Weberdy agent logic
↓
Response returned to chat UI


4. IPFS Node
------------

IPFS daemon running.

Commands used:

ipfs daemon


Interfaces:

WebUI
http://127.0.0.1:5001/webui

Gateway
http://127.0.0.1:8080/ipfs/


5. IPFS Deployment
------------------

Current CID:

QmRAnyDwRXbgGhKbzC45EevnHBnozEBU4BDFH9vE5NAxCM


Interface accessible through gateway:

http://127.0.0.1:8080/ipfs/QmRAnyDwRXbgGhKbzC45EevnHBnozEBU4BDFH9vE5NAxCM


Current Problem
===============

Frontend loads successfully from IPFS but cannot reach the backend API.

Error seen in chat interface:

Error: Could not reach Weberdy API


Diagnosis
=========

Backend server is running.

Ports observed:

8000
8001

Frontend fetch path likely incorrect or pointing to wrong port.


Next Step
=========

Test backend endpoint directly.

Example test request:

curl -X POST http://127.0.0.1:8000/v1/prompt \
-H "Content-Type: application/json" \
-d '{"message":"Hello Weberdy"}'


Goal
====

Fix frontend fetch connection so chat interface communicates with the FastAPI backend.


Project Vision
==============

XRPL Adaptive Autonomous DAO Avatar

Architecture:

AI Agent
+
FastAPI API
+
Web3 Frontend
+
IPFS Distributed Hosting


Status
======

95% complete.

Remaining task:

Fix frontend → backend connection.
