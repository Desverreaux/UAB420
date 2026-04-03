import hmac 
import os
import hashlib
import subprocess 
import requests 
from dotenv import load_dotenv 
from fastapi import FastAPI, Request, HTTPException 
from fastapi.middleware.cors import CORSMiddleware # Is required to allow cross-origin requests


load_dotenv()  # Load environment variables from .env file
gitApp = FastAPI() # Create FastAPI app

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
REPO_PATH = os.getenv("REPO_PATH")

@gitApp.post("/webhook") # GitHub webhook endpoint
async def webhook(request: Request):
    # Verify the request is actually from GitHub
    signature = request.headers.get("X-Hub-Signature-256")
    body = await request.body()
    
    expected = "sha256=" + hmac.new(
        WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(signature, expected):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Run git pull
    subprocess.run(["git", "restore", "."], cwd=REPO_PATH) # Restore the repo to discard any local changes before pulling
    subprocess.run(["git", "pull"], cwd=REPO_PATH)

    return {"status": "pulled"}
