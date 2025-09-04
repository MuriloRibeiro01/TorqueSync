# File for the database configs and connection.

# Imports MySQL Connector.
import mysql.connector
from mysql.connector import errorcode

# Imports for the security.
import os # The module is imported to comunicate with the operating system.
from dotenv import load_dotenv # Import to load the .env file.

# Load the .env file's variables.
load_dotenv

# Here is going to be the key to connect with the database.
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# Function to connect with the database.
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    
    except mysql.connector.Error as err:

        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro: Usuário ou senha inválidos")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Erro: Banco de dados não existe")
        else:
            print(err)
        return None