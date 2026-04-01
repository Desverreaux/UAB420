import mysql.connector
import boto3
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Database:
    def __init__(self):
        # Uses the load_dotenv package to load database credentials from a .env file,
        # it is set up this way so that we don't push our database creditials to GitHub 
                "host": os.getenv("DB_HOST"),
                "user": os.getenv("DB_USER"),
                "password": os.getenv("DB_PASSWORD"),
                "database": os.getenv("DB_NAME"),
                "port": 3306 # Default MySQL port it doesn't have to be obfuscated, so the value is just here
        }
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

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        """Reuses the open connection for each call"""
        cur = self.connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        cur.close()
        return result            