import hmac 
import os
import hashlib
import subprocess 
import requests 
import database
from dotenv import load_dotenv 
from fastapi import FastAPI, Request, HTTPException 
from fastapi.middleware.cors import CORSMiddleware # Is required to allow cross-origin requests


# Import packages information:
# HMAC, hashlib: Used for verifying the authenticity of incoming webhook requests from GitHub by creating a hash of the request body and comparing it to the signature provided in the request headers.
# OS: Used for accessing environment variables, such as API keys, which can be stored in a .env file for security and convenience.
# subprocess: Used for running shell commands, such as "git pull", to update the server code when a webhook is received from GitHub.
# requests: Used for making HTTP requests to external APIs, such as the lorem ipsum generator API, to fetch data that can be returned to the frontend.
# dotenv: Used for loading environment variables from a .env file, which allows you to keep sensitive information like API keys out of your codebase and easily manage them in a separate file.
# fastapi: Used for creating the FastAPI app, defining API endpoints, handling incoming requests, and raising HTTP exceptions when needed.              

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

#poop from a butts

################
# API ENDPOINTS
################

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

@app.get("/api/getHistoricalData")




# @app.get("/api/SendMoistureData")
# async def send_moisture_data(moistureLevel: float = None, plantID: int = 0):
#     try: 
#         if moistureLevel is None:
#             raise HTTPException(status_code=400, detail="moistureLevel query parameter is required")
#         query = "INSERT INTO moisture_data (plant_id, moisture_level) VALUES (%s, %s)"
#         params = (plantID, moistureLevel)
#         db.execute_query(query, params)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to insert moisture data: {e}")

#     return {"message": "Moisture data sent"}

@app.get("/api/db-test")
async def db_test():
    try:
        data = db.execute_query("SELECT first_name FROM employees")
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")


#########
# EVENTS
#########

@app.on_event("startup")
def startup():
    global db
    db = database.Database()
    db.connect()
    print("Database connected successfully")

@app.on_event("shutdown")
def shutdown():
    db.disconnect()

# TODO:

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
