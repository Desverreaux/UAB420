import mysql.connector
import boto3
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Database:
    def __init__(self):
        self.password = os.getenv("DB_PASSWORD")
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='uab-420-database.crfsezwej2qz.us-east-1.rds.amazonaws.com',
                port=3306,
                database='UAB420',
                user='admin',
                password=self.password,
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