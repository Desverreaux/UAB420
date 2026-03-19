import hmac
import hashlib
import subprocess
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

WEBHOOK_SECRET = "secret"
REPO_PATH = "/sharedFiles/Server"


app = FastAPI()

# Allow Vue dev server to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allows all origins, you can specify your frontend URL here
    allow_methods=["*"], # allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"], # allows all headers, you can specify which headers are allowed if needed
)

@app.post("/webhook")
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
    subprocess.run(["git", "pull"], cwd=REPO_PATH)
    return {"status": "pulled"}


@app.get("/api/hello")
async def hello():
    return {"message": "Hello from FastAPI!"}



