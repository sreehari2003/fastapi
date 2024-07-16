from pydantic import BaseModel
import boto3
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
secret_name = os.getenv("secret_name")
region_name = os.getenv("region_name")
pg_endpoint = os.getenv("pg_endpoint")
port = int(os.getenv("port"))

class Item(BaseModel):
    name: str
    description: str = None

def get_secret():
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        print(f"Error retrieving secret: {e}")
        return None

    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

credentials = get_secret()
if credentials:
    db_username = credentials['username']
    db_password = credentials['password']
else:
    print("Failed to retrieve credentials")
    exit()

def get_db_connection():
    try:
        connection = psycopg2.connect(
            user=db_username,
            password=db_password,
            host=pg_endpoint,
            port=port,
            cursor_factory=RealDictCursor
        )
        print("Connecting to database")
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

db = get_db_connection()

if db:
    print("Database connection successful")
else:
    print("Database connection failed")
