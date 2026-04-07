import inspect
import functools
from dateutil import parser
from fastapi import HTTPException


######################
# Validation Functions
######################

def validateTimestamp(timestamp): #todo finish this function, as it currently consolidates different ways of writting a timestamp but doesn't actually check if it is a time stamp
	try:
		return parser.parse(timestamp)
	except (TypeError, ValueError):
		raise HTTPException(status_code=400, detail="Bad request: invalid timestamp")

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
	
	dataObject.plantId = validatePlantId(dataObject.plantId)
	dataObject.moistureLevel = validateMoistureLevel(dataObject.moistureLevel)

	if hasattr(dataObject, "timestamp") and dataObject.timestamp is not None:
		dataObject.timestamp = validateTimestamp(dataObject.timestamp)
	
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
	except TypeError: #Catches exceptions throw as a result of no input
		raise HTTPException(status_code=400, detail="Bad request: A value was not provided for plantID")


######################
# Decorator
######################

# Map parameter names to their validation functions
# It can be read as if a function uses the arguement "moistureData" then auto_validate will call validateMoistureData on that value before passing it to the original funciton
VALIDATORS = {
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
