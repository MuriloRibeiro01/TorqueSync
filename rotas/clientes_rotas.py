# Imports for the clients routes.
from flask import Blueprint, jsonify, request
from db import get_db_connection

# Create a Blueprint for client routes
clientes_bp = Blueprint('clientes_bp', __name__)

# Route to search all clients.
@clientes_bp.route('/api/clientes', methods=['GET'])
def get_clientes():
    try:
        # Opens the Cursor to comunicate with the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Gets all clients from the table.
        query = "SELECT * FROM clientes"
        cursor.execute(query)

        # Gets all results returned from the database.
        clientes = cursor.fetchall()

        # Returns the clients list in JSON format, if no error occursed.
        return jsonify(clientes)
    except Exception as e:
        # If any error occurs:
        print(f"Erro ao buscar clientes: {e}")
        return jsonify({"error": "Erro interno no servidor"}), 500
    finally:
        # Closes Cursor, if it works or not.
        if 'cursor' in locals() and cursor is not None:
            cursor.close