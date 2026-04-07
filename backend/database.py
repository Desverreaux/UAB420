import mysql.connector
import boto3
import os
import time
from functools import wraps
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Database:
    def __init__(self):
        # Uses the load_dotenv package to load database credentials from a .env file,
        # it is set up this way so that we don't push our database creditials to GitHub 
        self.credintials = {
                "host": os.getenv("DB_HOST"),
                "user": os.getenv("DB_USER"),
                "password": os.getenv("DB_PASSWORD"),
                "database": os.getenv("DB_NAME"),
                "port": 3306 # Default MySQL port it doesn't have to be obfuscated, so the value is just here
        }
        print("Database credentials loaded successfully")
        print(f"Database host: {self.credintials['host']}")
        print(f"Database user: {self.credintials['user']}")
        print(f"Database name: {self.credintials['database']}") 
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.credintials["host"],
                port=self.credintials["port"],
                database=self.credintials["database"],
                user=self.credintials["user"],
                password=self.credintials["password"],
                ssl_disabled=False,
                autocommit=True,
                ssl_ca='../global-bundle.pem'
            )
        except Exception as e:
            print(f"Database error: {e}")
            raise


    # Decorator that automatically sanitizes all arguments passed to a function.
    # Place @auto_sanitize above any method to have its inputs cleaned before the method runs.
    # It detects the type of each argument (int, float, string) and runs sanitize() on it.
    # This means you don't have to manually call sanitize() inside every method.
    def auto_sanitize(func):
        @wraps(func) # Preserves the original function's name and docstring for debugging
        def wrapper(self, *args, **kwargs):
            # Sanitize positional arguments (e.g., addPlant("Fern", "Kitchen"))
            clean_args = []
            for val in args:
                if isinstance(val, int):
                    clean_args.append(self.sanitize(val, "int"))
                elif isinstance(val, float):
                    clean_args.append(self.sanitize(val, "float"))
                elif isinstance(val, str):
                    clean_args.append(self.sanitize(val, "string"))
                else:
                    clean_args.append(val) # Leave unknown types (None, datetime, etc.) as-is

            # Sanitize keyword arguments (e.g., addPlant(plantName="Fern"))
            clean_kwargs = {}
            for key, val in kwargs.items():
                if isinstance(val, int):
                    clean_kwargs[key] = self.sanitize(val, "int")
                elif isinstance(val, float):
                    clean_kwargs[key] = self.sanitize(val, "float")
                elif isinstance(val, str):
                    clean_kwargs[key] = self.sanitize(val, "string")
                else:
                    clean_kwargs[key] = val

            # Call the original function with the cleaned arguments
            return func(self, *clean_args, **clean_kwargs)
        return wrapper

    # Validates a single value based on its expected type.
    # Called automatically by auto_sanitize, but can also be called manually.
    # - Checks that the value matches the expected type (int, float, or string)
    # - For strings: strips whitespace, enforces max length, rejects empty strings,
    #   and blocks SQL injection keywords/patterns even if someone forgets to use %s params
    # - Returns the cleaned value, or raises a ValueError if validation fails
    def sanitize(self, value, value_type="string", max_length=255):
        
        if value is None: # Allow None values to pass through (for optional arguments)
            return None

        if value_type == "int":
            if not isinstance(value, int): # Reject non-integer values like "abc" or 3.14
                raise ValueError(f"Expected int, got {type(value).__name__}")
            return value

        if value_type == "float":
            if not isinstance(value, (int, float)): # Accept both int and float, reject strings
                raise ValueError(f"Expected float, got {type(value).__name__}")
            return float(value) # Convert int to float for consistency

        if value_type == "string":
            value = str(value).strip() # Remove leading/trailing whitespace (e.g., "  Fern  " → "Fern")
            if len(value) > max_length: # Prevent excessively long strings from being stored
                raise ValueError(f"Input exceeds max length of {max_length}")
            if len(value) == 0: # Reject empty strings after stripping
                raise ValueError("Input cannot be empty")

            # --- SQL Injection Protection ---
            # This is a safety net in case someone writes raw f-string queries instead of parameterized queries.
            # Parameterized queries (%s) are the RIGHT way to prevent injection, but this catches it if they don't.
            
            import re
            # Block common SQL injection keywords (case-insensitive, must be standalone words)
            # \b = word boundary, so "DROP" is blocked but "backdrop" is not
            sql_keywords = [
                r"\bDROP\b", r"\bDELETE\b", r"\bINSERT\b", r"\bUPDATE\b",
                r"\bSELECT\b", r"\bUNION\b", r"\bALTER\b", r"\bCREATE\b",
                r"\bEXEC\b", r"\bEXECUTE\b", r"\bTRUNCATE\b", r"\bGRANT\b",
                r"\bREVOKE\b", r"\bSHUTDOWN\b",
            ]
            for pattern in sql_keywords:
                if re.search(pattern, value, re.IGNORECASE):
                    raise ValueError(f"Input contains forbidden SQL keyword: {value}")

            # Block dangerous characters commonly used in SQL injection
            # ; = statement terminator, -- = comment, /* */ = block comment
            # ' and " could be used to break out of a string in a raw query
            dangerous_patterns = [
                r";",           # Statement terminator (e.g., "Fern; DROP TABLE plants")
                r"--",          # SQL comment (e.g., "admin'--")
                r"/\*",         # Block comment open
                r"\*/",         # Block comment close
                r"\\",          # Backslash escape
                r"'",           # Single quote (used to break out of SQL strings)
                r"\"",          # Double quote
                r"\bOR\b\s+\b\d+\b\s*=\s*\b\d+\b",  # Classic "OR 1=1" pattern
                r"\bAND\b\s+\b\d+\b\s*=\s*\b\d+\b",  # "AND 1=1" pattern
            ]
            for pattern in dangerous_patterns:
                if re.search(pattern, value, re.IGNORECASE):
                    raise ValueError(f"Input contains potentially dangerous characters: {value}")

            return value

    @auto_sanitize
    def getHistoricalData(self, plantID: int = None, fromDate: time, toDate: time):
        #this will get called so we can make a little graph on the front end, it just returns the last however many (there should be some upper limit) moisture level readings for a plant
        #return type should be a json file 
        pass

    @auto_sanitize
    def getLast*Event*(self, plantID: int = None, event: string):
        #this will search the readings of a given plant and return the last time an *event* happened 
        #im imagining this as like you pass "dry", and it would return the last time the plant had its moisture drop below 10% or something 
        #you can also have the event string be like a argument that you parse, kinda like the reflextor assignment we had, but that sounds hard
        #you can also make this into several functions thats why i added the * around event, so like you'd have getLastWatering, getLastDryiest, etc
        #events could be: Last time watered, last time it was really dry, ... i feel like there would be others but can't think of any 
        #return type should be a timestamp
        pass

    @auto_sanitize
    def logMeasurement(self, plantID: int = None, moistureLevel: float, timestamp: time):
        #so the main.py (name might have changed) is going to get moisture data from the pico, its then gonna call this function to save that data to the database
        #should check that arguments are filled and throw an error if they arent
        #sql has an option to just make a time stamp when a entry is created if you want to use that or pass your own timestamp is up to up
        #return type should be some kind of confirmation that the value was sent in
        pass

    @auto_sanitize
    def getMoistureLevel(self, plantID: int = None):
        #this will return the most recent moisture reading for a plant 
        #return type will be a float 
        pass 

    @auto_sanitize
    def addPlant(self, plantID: int = None, plantName: string = None, plantRoom: string = None) 
        #this will add a plant to the database 
        pass

    @auto_sanitize
    def getPlants(self):
        #this will return a list of all the plants we got
        pass

    @auto_sanitize
    def getPlantName(self, plantID: int = None):
        #returns the name of the plant given its ID
        pass

    @auto_sanitize
    def getPlantIdByName(self, Name: string = ""):
        #probably isn't required but would search for a plant named "blah" and return the primary key for that entry
        pass

    @auto_sanitize
    def getPlantStatus(self, plantID: int = None): 
        #based on nik's wireframe, we'll have a health attribute to the plant
        #apparently the options are healthy, needs attention, and struggling 
        pass

    @auto_sanitize
    def setPlantStatus(self, plantID: int = None, status: string = ""):
        #a setter for the health status, status needs to be validated to make sure its one of the options
        pass

    @auto_sanitize
    def setPlantImagePath(self, plantID: int = None, pathToPlantImage: string = "", plantSpecies):
        # the absolute parent path to the images is gonna be /sharedFiles/Server/frontend/src/assets/Images/Plants
        # the relative parent path to the images is gonna be ../frontend/src/assets/Images/Plants
        # this will store the filepath of the image for a species of plant

    @auto_sanitize
    def getPlantImagePath(self, plantSpecies: str = None):
        # this will get the file path for the image for a given type of plant 
  
    @auto_sanitize
    def getPlantRoom(self, plantID: int = None):
        pass

    @auto_sanitize
    def setPlantRoom(self, plantID: int = None):
        pass 

    @auto_sanitize
    def addUser(self, userName: string = None, password: string = ""):
        #this will add a username and password to your implementation of a users table 
        pass

    @auto_sanitize
    def isUser(self, userName: string = None, password: string = ""):
        #this will be used to validate the creditials of a login, you get the username and password, find the user in the table, and compare the password to the password given 
        #im sure theres a fancy way of hashing/encrypting the password for security purposes, but i don't think thats really nesscesary 
        pass  

    @auto_sanitize
    def getUserData(self, userName: string = None): 
        #according to nik's diagram users will have attributes like climate, and preferred units of temperature you can either make these their own column and have getters and setters for each
        #or if we wanna be flexable we can just have a Data column that holds some json that holds all the attributes like that
        pass

    @auto_sanitize
    def setUserData(self, userName: string = None, attribute: string, value):
        #setter for the thing above 
        pass

    #Tables needed Users, Readings, Plants, Images
    #### Users needs columns: id, username, password, unit of temp prefference, climate, whatever else you can thing of
    #### Readings needs columns: id, moistureLevel, plantId, timestamp
    #### Plants needs columns: id, plantName, mostRecentMoistureLevel(maybe?), room, plantSpecies, plantImage, status
    #### Images needs columns: id, plantSpecies, filepath, (some kind of hash so you can check if the image is still at that location, optional tho cause i have no idea how to do that)
    #### ----Note: Images only stores the file path of the images as that just stores better, like its possible to store the images in the database but it would make the code alot more annoying and slower    
    


    def disconnect(self):
        if self.connection:
            self.connection.close()

    @auto_sanitize
    def execute_query(self, query, params=None):
        """Reuses the open connection for each call"""
        cur = self.connection.cursor()
        cur.execute(query, params)
        result = cur.fetchall()
        cur.close()
        return result            