import mysql.connector
 
mydb = mysql.connector.connect(
    host="localhost",
    user="ptlabadie",
    password="koEAe9Nd2nzckP",
    database="QUESTRADE"
)
 
mycursor = mydb.cursor()
 
mycursor.execute("Show tables;")
 
myresult = mycursor.fetchall()
 
for x in myresult:
    print(x)

mycursor.close()
# # MySQL connection details
# username = 'ptlabadie'
# password = 'koEAe9Nd2nzckP'
# hostname = 'localhost'
# port = '3306'
# database_name = 'QUESTRADE'

# # create a connection string using the format 'mysql+pymysql://<username>:<password>@<host>:<port>/<database>'
# connection_string = f'mysql+pymysql://{username}:{password}@{hostname}:{port}/{database_name}'
# # create SQLAlchemy engine object
# engine = create_engine(connection_string)

# mycursor.execute("Show tables;")
 
# myresult = mycursor.fetchall()
 
# for x in myresult:
#     print(x)

