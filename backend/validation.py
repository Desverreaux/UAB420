import inspect
import functools
from dateutil import parser
from fastapi import HTTPException


######################
# Validation Functions
######################

def validateUserName(username):
	if len(username) < 0:
		raise HTTPException(status_code=401, detail="Error: Username must be at least 1 character")
	if len(username) > 32:
		raise HTTPException(status_code=401, detail="Error: Username must be at less than 32 characters")
	return username 

def validatePassword(password): 
	if len(password) > 32:
		raise HTTPException(status_code=401, detail="Error: Password must be at less than 32 characters")
	return password 

def validateTimestamp(timestamp):
	"""
	Accepts:
	  - None            → returns None (let the endpoint apply its own default)
	  - numeric / numeric string like 0, 1741814400 → treated as a Unix epoch (seconds)
	  - human-readable string like "march 12th 2012" or "1/1/1 1:1:1" → parsed by dateutil
	Always returns a float (epoch seconds) or None.
	"""
	if timestamp is None:
		return None

	# If it's already a number, treat it as epoch seconds
	if isinstance(timestamp, (int, float)):
		return float(timestamp)

	# If it's a string, try numeric first, then natural-language parsing
	if isinstance(timestamp, str):
		try:
			return float(timestamp)  # handles "0", "1741814400", etc.
		except ValueError:
			pass
		try:
			dt = parser.parse(timestamp)          # handles "march 12th 2012", "1/1/1 1:1:1", etc.
			return dt.timestamp()                  # convert to epoch float
		except (ValueError, OverflowError):
			raise HTTPException(status_code=400, detail=f"Bad request: '{timestamp}' is not a valid timestamp")

	raise HTTPException(status_code=400, detail=f"Bad request: invalid timestamp type '{type(timestamp).__name__}'")

def validateMoistureLevel(moistureLevel): 
	try:
		moistureLevel = float(moistureLevel) #checks to see if moistureLevel is a float or can be cast as a float
		if 0 <= moistureLevel <= 1:  #checks to see if moistureLevel is between 0 and 1 sense it is suppose to be a percent value 
			return moistureLevel
		else:
			raise HTTPException(status_code=400, detail=f"Bad request: moistureLevel must be between 0 and 1, got {moistureLevel}")
	except (TypeError, ValueError):
		raise HTTPException(status_code=400, detail=f"Bad request: '{moistureLevel}' is not a valid number")

def validateMoistureData(dataObject):
 
	valuesToCheck = ["plantId", "moistureLevel"]

	if dataObject is None:
		raise HTTPException(status_code=400, detail="Bad request: No data was sent")
	for value in valuesToCheck:
		if value not in dataObject:
			raise HTTPException(status_code=400, detail=f"Bad request: Missing required field '{value}'")
	
	dataObject["plantId"] = validatePlantId(dataObject["plantId"])
	dataObject["moistureLevel"] = validateMoistureLevel(dataObject["moistureLevel"])

	if hasattr(dataObject, "timestamp") and dataObject["timestamp"] is not None:
		dataObject["timestamp"] = validateTimestamp(dataObject["timestamp"])
	
	return dataObject

def validatePlantId(plantIdentifier):
	try:
		if type(plantIdentifier) == int:
			return plantIdentifier
		elif type(plantIdentifier) == str: #In this case the plant is being referred to by either its name, or a string of "38" for example
			#this try catch block essentially works as a if/else statement for whether the variable is a string or a int
			try:
				plantId = int(plantIdentifier) #attempts to convert the string into an int, this checks if the id just got passed as a string somehow
				return plantId #if the above line executes without throwing an error then the identifier was a number passed as a string
			except ValueError:
				return plantIdentifier # return the string name as-is for now, database lookup can happen in the endpoint
		else: 
			raise HTTPException(status_code=400, detail="Bad request: plantid must either be an int or the name of the plant")	
	except TypeError: #Catches exceptions throw as a result of no input
		raise HTTPException(status_code=400, detail="Bad request: A value was not provided for plantID")


######################
# Decorator
######################

# Map parameter names to their validation functions
# It can be read as if a function uses the arguement "moistureData" then auto_validate will call validateMoistureData on that value before passing it to the original funciton
VALIDATORS = {
	"username": validateUserName,
	"password": validatePassword,
	"moistureLevel": validateMoistureLevel,
	"moistureData": validateMoistureData,
	"plantIdentifier": validatePlantId,      # validates and resolves plant IDs
	"fromDate": validateTimestamp,            # parses timestamps
	"toDate": validateTimestamp,
}

#this defines a decorator that will read the argument names of a function and call a appropreate validator method on the value passed throught that argument 
def auto_validate(func):
	@functools.wraps(func) #this is another decorater that corrects how function names are called later
	async def wrapper(*args, **kwargs): 
		sig = inspect.signature(func) #read the names of the arguments passed into the function
		bound = sig.bind(*args, **kwargs)
		bound.apply_defaults()

		for param_name, value in bound.arguments.items():
			if param_name in VALIDATORS:
				bound.arguments[param_name] = VALIDATORS[param_name](value)

		return await func(*bound.args, **bound.kwargs)
	return wrapper
