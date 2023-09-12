import boto3
import pickle
import mysql.connector
import pandas as pd
import os, pickle, pandas as pd
from sqlalchemy import create_engine, text
import csv
import toml

# # Set up AWS credentials

secrets = toml.load(".gitignore\secrets.toml")
print(secrets)
ACCESS_KEY = secrets['ACCESS_KEY']
SECRET_KEY = secrets['SECRET_KEY']

# SESSION_TOKEN = 'your-session-token'  # Optional if you have a session token

# Create an S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
    # aws_session_token=SESSION_TOKEN
)

# Specify the bucket name and file name
bucket_name = 'intraday-dashboard'
file_name = 'eq_AAPL.csv'

# Download the file from the S3 bucket
s3.download_file(bucket_name, file_name, file_name)

# Process the file as needed

df = pd.read_csv(file_name)


print(df)
    # Process the data here