# Split up each most recently pulled data into {SYMBOL}.CSV
# In main.py, instead of pickle, call to s3 bucket. 

import glob
import os 
import pickle
import os, pickle, pandas as pd
from sqlalchemy import create_engine, text
import boto3

import os

import toml

# # Set up AWS credentials

secrets = toml.load(".gitignore/secrets.toml")
print(secrets)
ACCESS_KEY = secrets['ACCESS_KEY']
SECRET_KEY = secrets['SECRET_KEY']

def separate_eq_sql_to_csv():

    # Delete all csv files in ...dashboard/data, these will be old data
    mydir = "C:/Users/Patrick/Documents/projects/intraday-financial-dashboard/data/equities/"
    filelist = [ f for f in os.listdir(mydir) if f.endswith(".csv") ]
    for f in filelist:
        os.remove(os.path.join(mydir, f))
    
    
    # MySQL connection details
    username = 'ptlabadie'
    password = 'koEAe9Nd2nzckP'
    hostname = 'localhost'
    port = '3306'
    database_name = 'QUESTRADE'

    # create a connection string using the format 'mysql+pymysql://<username>:<password>@<host>:<port>/<database>'
    connection_string = f'mysql+pymysql://{username}:{password}@{hostname}:{port}/{database_name}'
    # create SQLAlchemy engine object
    engine = create_engine(connection_string)
    # Create query to get the tablename of the 2 most recently created tables
    recent_tbl_query = "select table_name, create_time from information_schema.TABLES where table_schema = 'QUESTRADE' order by CREATE_TIME desc limit 2"
    table_name_df = pd.DataFrame(engine.connect().execute(text(recent_tbl_query)))
    equity_table = (table_name_df['TABLE_NAME'][0]) 



    # use table_name variable to get table as pandas df

    ## for equities
    equity_query = "select * from " + equity_table
    equity_df = pd.DataFrame(engine.connect().execute(text(equity_query)))
    equity_syms =  list(equity_df['symbol'].unique())
    for sym in equity_syms:
    #     # csv location: C:/Users/Patrick/Documents/projects/dashboard/data
    #     # csv name: "C:/Users/Patrick/Documents/projects/dashboard/data/equity"+sym+".csv"
    #     # separate df: 
        out_file = mydir + "/eq_" + sym + ".csv"
        equity_df.loc[equity_df['symbol'] == sym].to_csv(out_file)


    engine.dispose()
    return None



def separate_opt_sql_to_csv():

    # Delete all csv files in ...dashboard/data, these will be old data
    mydir = "C:/Users/Patrick/Documents/projects/intraday-financial-dashboard/data/options/"
    filelist = [ f for f in os.listdir(mydir) if f.endswith(".csv") ]
    for f in filelist:
        os.remove(os.path.join(mydir, f))
    
    
    # MySQL connection details
    username = 'ptlabadie'
    password = 'koEAe9Nd2nzckP'
    hostname = 'localhost'
    port = '3306'
    database_name = 'QUESTRADE'

    # create a connection string using the format 'mysql+pymysql://<username>:<password>@<host>:<port>/<database>'
    connection_string = f'mysql+pymysql://{username}:{password}@{hostname}:{port}/{database_name}'
    # create SQLAlchemy engine object
    engine = create_engine(connection_string)
    # Create query to get the tablename of the 2 most recently created tables
    recent_tbl_query = "select table_name, create_time from information_schema.TABLES where table_schema = 'QUESTRADE' order by CREATE_TIME desc limit 2"
    table_name_df = pd.DataFrame(engine.connect().execute(text(recent_tbl_query)))
    options_table = (table_name_df['TABLE_NAME'][1]) 
    print(options_table)

    ## for options
    opt_query = "select * from " + options_table
    opt_df = pd.DataFrame(engine.connect().execute(text(opt_query)))
    print(opt_df.head())
    opt_syms =  list(opt_df['underlying'].unique())
    print(opt_syms)
    # separate each company by sym, save it as a csv file
    
    for sym in opt_syms:
    #     # csv location: C:/Users/Patrick/Documents/projects/dashboard/data
    #     # csv name: "C:/Users/Patrick/Documents/projects/dashboard/data/equity"+sym+".csv"
    #     # separate df: 

        out_file = mydir + "/opt_" + sym + ".csv"
        opt_df.loc[opt_df['underlying'] == sym].to_csv(out_file)
    engine.dispose()
    return None


separate_eq_sql_to_csv()
separate_opt_sql_to_csv()



def delete_s3_bucket_csv():
    # Upload each {SYMBOL}.CSV to amazon s3 bucket
    # # Set up AWS credentials
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    # path = "C:/Users/Patrick/Documents/projects/dashboard/data/equities/eq_TRGP.csv"
    # file_name = os.path.basename(path)
    # s3.upload_file(path,"questrade-bucket" , file_name)


    # List all objects in the bucket
    objects = s3.list_objects(Bucket="intraday-dashboard")

    # Loop through the objects and delete CSV files
    for obj in objects.get('Contents', []):
        if obj['Key'].lower().endswith('.csv'):
            print(f"Deleting {obj['Key']}")
            s3.delete_object(Bucket="intraday-dashboard", Key=obj['Key'])

    print("CSV files deleted.")

# delete_s3_bucket_csv()


def upload_all_files_to_s3():

    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    optdir = "C:/Users/Patrick/Documents/projects/intraday-financial-dashboard/data/options/"
    eqdir = "C:/Users/Patrick/Documents/projects/intraday-financial-dashboard/data/equities/"
    optlist = [ f for f in os.listdir(optdir) if f.endswith(".csv") ]
    eqlist = [ f for f in os.listdir(eqdir) if f.endswith(".csv") ]



    for f in optlist:
        filepath = optdir+f
        print(filepath)
        file_name = os.path.basename(filepath)
        s3.upload_file(filepath, "intraday-dashboard", file_name)

    for f in eqlist:
        filepath = eqdir+f
        print(filepath)
        file_name = os.path.basename(filepath)
        s3.upload_file(filepath, "intraday-dashboard", file_name)
    return None

delete_s3_bucket_csv()
upload_all_files_to_s3()