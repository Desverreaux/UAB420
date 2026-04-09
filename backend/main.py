import hmac 
import os
import time
import hashlib
import subprocess 
import requests 
import database
# import bcrypt
import fakeModels as fake
from dateutil import parser
from dotenv import load_dotenv 
from fastapi import FastAPI, Request, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware # Is required to allow cross-origin requests
from validation import auto_validate, validatePlantId, validateMoistureData
from pydantic import BaseModel

# Import packages information:
# HMAC, hashlib: Used for verifying the authenticity of incoming webhook requests from GitHub by creating a hash of the request body and comparing it to the signature provided in the request headers.
# OS: Used for accessing environment variables, such as API keys, which can be stored in a .env file for security and convenience.
# subprocess: Used for running shell commands, such as "git pull", to update the server code when a webhook is received from GitHub.
# requests: Used for making HTTP requests to external APIs, such as the lorem ipsum generator API, to fetch data that can be returned to the frontend.
# dotenv: Used for loading environment variables from a .env file, which allows you to keep sensitive information like API keys out of your codebase and easily manage them in a separate file.
# fastapi: Used for creating the FastAPI app, defining API endpoints, handling incoming requests, and raising HTTP exceptions when needed.              

REPO_PATH = "/sharedFiles/Server"

# class MoistureData(BaseModel):
#     plantIdentifier: str
#     moistureLevel: float
#     timestamp: float = None  # optional, defaults to None



load_dotenv()  # Load environment variables from .env file
app = FastAPI() # Create FastAPI app

# Allow Vue dev server to talk to FastAPI
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],  # allows all origins, you can specify your frontend URL here
	allow_methods=["*"], # allows all HTTP methods (GET, POST, etc.)
	allow_headers=["*"], # allows all headers, you can specify which headers are allowed if needed
)

################
# API ENDPOINTS
################

# GENERAL NOTES:
# the variable "plantIdentifier" works for either the plant name or the plant id, 

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

@app.get("/api/getHistoricalData", status_code=200)
@auto_validate
async def get_historical_data(plantIdentifier, fromDate, toDate):

	# Sets defaults for time frame if none is provided, defaults to from the beginning of time to now 
	if fromDate is None:
		fromDate = 0  # represents the epoch so 1970  
	if toDate is None:
		toDate = time.time()  # represents the current time 
	
	data = db.getHistoricalData(plantIdentifier, fromDate, toDate)
	return {"data": data}

@app.get("/api/getPlantData")
@auto_validate
async def get_plant_data(plantIdentifier):

	data = db.getPlantData(plantIdentifier)
	
	return {"data": FakeModels.plant(plantID=1)}
	# return {"data": data}


@app.post("/api/SendMoistureData", status_code=201)
@auto_validate
async def send_moisture_data(moistureData: dict = Body()):

	if "timestamp" not in moistureData or moistureData["timestamp"] is None:
		moistureData["timestamp"] = time.time()

	# db.logMeasurement(moistureData["plantId"], moistureData["moistureLevel"], moistureData["timestamp"])

	return {"message": "Moisture data sent"}

@app.post("/api/createUser", status_code=201)
@auto_validate
async def createNewUser(username: str, password: str):
	if(db.isUser(username)):
		raise HTTPException(status_code=400, detail=f"Error: User already exists")
	db.addUser(username,password)
	return {"message": f"Account for {username} has been created!"}

@app.post("/api/login", status_code=200)
@auto_validate
async def login(username: str, password: str):
	if(not db.isUser(username)): 
		raise HTTPException(status_code=401, detail=f"Error: User doesn't exist!")
	elif (db.getPassword(username) != password): 
		raise HTTPException(status_code=401, detail=f"Error: Incorrect Password!")
	else: 
		return {"message": f"User:{username} successfully logged in!"}

@app.get("/api/getUserData", status_code=200)
@auto_validate
async def getUserData(username: str):
	if(not db.isUser(username)): 
		raise HTTPException(status_code=401, detail=f"Error: User doesn't exist!")
	else: 
		data = db.getUserData(username)
		return {"data": data}






		

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

##################
# Helper Functions 
##################

def hash_password(plain_password: str):
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed: str):
    return bcrypt.checkpw(plain_password.encode(), hashed.encode())

# TODO:

# Set up positive http codes 


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
