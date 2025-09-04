# Imports 'wraps'
from functools import wraps

# Imports Blueprint from Flask
from flask import Blueprint

# Imports Flask and others usifull tools.
from flask import Flask, jsonify, request

# Imports CORS.
from flask_cors import CORS

# Impots MySQL Connector.
import mysql.connector



# Create the instance of the application.
app = Flask(__name__)
CORS(app) # Starts CORS.   


# Row to run the application in administrator mode.
if __name__ == '__main__':
    app.run(debug=True)


# Ideias de melhorias:
# Adicionar número do ID dos veículos.
# Ao apagar um dos veículos, automaticamente transformar o próximo veículo naquele ID qual foi apagado.