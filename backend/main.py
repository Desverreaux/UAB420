import hmac
import os
import hashlib
import subprocess
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

WEBHOOK_SECRET = "secret"
REPO_PATH = "/sharedFiles/Server"

load_dotenv()  # Load environment variables from .env file
app = FastAPI() # Create FastAPI app

# Allow Vue dev server to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allows all origins, you can specify your frontend URL here
    allow_methods=["*"], # allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"], # allows all headers, you can specify which headers are allowed if needed
)

@app.post("/webhook") # GitHub webhook endpoint
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


@app.get("/api/loremIpsum") # Example API endpoint to fetch lorem ipsum text
async def lorem_ipsum(wordCount: int = 20):
    headers = {
        "X-API-Key": os.getenv("NINJAS_API_KEY")  # Assuming you have an API key stored in your .env file
    }
    if wordCount < 1 or wordCount > 100:
        raise HTTPException(status_code=400, detail="wordCount must be between 1 and 100")
    else:    
        response = requests.get("https://api.api-ninjas.com/v1/loremipsum", params={"start_with_lorem_ipsum": True}, headers=headers)
    text = response.json().get("text", "") # Get the generated text from the API response, defaulting to an empty string if not found
    words = text.split()[:wordCount] # Split the text into words and take the specified number of words
    trimmed_text = " ".join(words) # Join the selected words back into a string
        
    return {"message": trimmed_text}




# TODO:
# get server connected to the database
# --- john will have to do this as it requires aws access and im not gonna set that up 
# get database tables set up 
# --- need a table for temperature measurements (measurements, timestamp, plantID, other stuff..)
# --- need a table for users if we are still doing that 
# get server connected to the raspberry pi
# --- set up api calls that the pi can call to send data to the server b  
# go through niks wireframes and figure out which data will need to be passed to the front end
# figure out a structure on how to pass data to the front end 
# --- like what the structure of the api calls to be 
# --- (...com/api/exampledata) with hard coded routes 
# --- (...com/api/data?type=example) with url variables
# --- (...com/api/data) with type=example as a parameter in the body of the get request
