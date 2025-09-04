# Imports somethings from the past file
from flask import Blueprint, jsonify, request

# Imports 'wraps'
from functools import wraps

# Imports the function to connect with the database.
from db import get_db_connection

# Create a Blueprint for vehicle routes
veiculos_bp = Blueprint('veiculos_bp', __name__)

# Creates an validator for the vehicles.
def validacao_veiculo_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        # First, it pulls the JSON data from the request.
        dados = request.get_json()

        # Second, it verifies the data.
        if not dados or 'placa' not in dados or 'modelo' not in dados:
            return jsonify({"error": "Dados incompletos. Placa e modelo são obrigatórios"}), 400  # 400 = Bad Request

        # Third, is everything is OK, it continues to the original route.
        return f(dados = dados, *args, **kwargs)
    return decorated_function

# Route to list the vehicles.
@veiculos_bp.route('/api/veiculos', methods=['GET'])
def get_veiculos():
    print("\n--- Rota /api/veiculos foi chamada! ---")

    conn = None  # Just to make sure the variable exists.
    try:
        print("1. Tentando conectar ao banco de dados...")
        conn = get_db_connection()
        print("2. Conexão com o banco bem-sucedida!")

        cursor = conn.cursor(dictionary=True)
        print("3. Objeto cursor criado com sucesso!")

        print("4. Executando a query 'SELECT * FROM veiculos'...")
        cursor.execute('SELECT * FROM veiculos')
        print("5. Query executada com sucesso!")

        veiculos = cursor.fetchall()
        print(f"6. Dados buscados. Total de registros: {len(veiculos)}")

        cursor.close()
        conn.close()
        print("7. Conexão com o banco fechada. Tentando retornar JSON...")

        return jsonify(veiculos), 200

    except Exception as e:
        # Basically is a test block, so... ignore it ;)
        # This block will catch any error and show it in the terminal.
        print("\n!!!!!! OCORREU UMA EXCEÇÃO NO BLOCO TRY !!!!!!")
        print(f"TIPO DO ERRO: {type(e)}")
        print(f"MENSAGEM DO ERRO: {e}\n")

        # Security block to ensure the connection is closed in case of error
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("Conexão de emergência com o banco foi fechada.")

        # Return the error to the frontend, but the terminal print is more important
        return jsonify({'error': str(e)}), 500

# Route to get a specify vehicle by ID.
@veiculos_bp.route('/api/veiculos/<int:id>', methods=['GET'])
def get_veiculo_por_id(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT * FROM veiculos WHERE id = %s', (id,))

        veiculo = cursor.fetchone() # fetchone() gets a single result

        cursor.close()
        conn.close()

        if veiculo:
            return jsonify(veiculo), 200
        else:
            return jsonify({"error": "Veículo não encontrado"}), 404 # 404 is the code to "not found"

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to create a new vehicle.
@veiculos_bp.route('/api/veiculos', methods=['POST'])
@validacao_veiculo_required
def criar_veiculo(dados):

    # Extracts the data from the JSON.
    placa = dados['placa']
    modelo = dados['modelo']
    ano = dados.get('ano') # The .get() is going to be more safe, cause returns None if the key doesn't exist
    cor = dados.get('cor')
    quilometragem = dados.get('quilometragem')
    status = dados.get('status', 'Disponível') # Sets the value as 'Disponível', an car that comes to the rental company is available by default.

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Query to insert a new vehicle.
        query = """
            INSERT INTO veiculos (placa, modelo, ano, cor, quilometragem, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        # Execute the query with the data in a tuple.
        cursor.execute(query, (placa, modelo, ano, cor, quilometragem, status))

        # Gets the ID of the newly added vehicle.
        novo_veiculo_id = cursor.lastrowid # Last Row ID

        # Confirms the changes in the database. Like and commit in Git.
        conn.commit()

        cursor.close()
        conn.close()

        # Now it going to return the object that was added.
        novo_veiculo_adicionado = {
            'id': novo_veiculo_id,
            'placa': placa,
            'modelo': modelo,
            'ano': ano,
            'cor': cor,
            'quilometragem': quilometragem,
            'status': status
        }
        return jsonify(novo_veiculo_adicionado), 201

    except Exception as e:
        # The rollback is going to undo any change in the database if an error occurs.
        if 'conn' in locals() and conn:
            conn.rollback()
        print(f"Erro ao criar veículo: {e}")
        return jsonify({"error": "Ocorreu um erro ao criar o veículo."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to update a vehicle. By the ID.
@veiculos_bp.route('/api/veiculos/<int:id>', methods=['PUT'])
@validacao_veiculo_required
def atualizar_veiculo(id, dados):
    placa = dados['placa']
    modelo = dados['modelo']
    ano = dados.get('ano')
    cor = dados.get('cor')
    quilometragem = dados.get('quilometragem')
    status = dados.get('status')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Query to update a vehicle. By the ID.
        query = """
            UPDATE veiculos 
            SET placa = %s, modelo = %s, ano = %s, cor = %s, quilometragem = %s, status = %s
            WHERE id = %s
        """

        # Execute the query with the data in a tuple.
        cursor.execute(query, (placa, modelo, ano, cor, quilometragem, status, id))

        conn.commit()

        # Verifies if any row was actually updated.
        if cursor.rowcount == 0:
            return jsonify({"error": "Veículo não encontrado"}), 404

        cursor.close()
        conn.close()

        # It returns an succes response.
        return jsonify({"message": "Veículo atualizado com sucesso!"}), 200 # 200 = OK

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to delete an vehicle. By the ID.
@veiculos_bp.route('/api/veiculos/<int:id>', methods=['DELETE'])
def deletar_veiculo(id):
    try:
        # 1. Opens the connection with the database.
        conn = get_db_connection()
        cursor = conn.cursor()

        # 2. Executes an SQL DELETE command for an vehicle with the given ID.
        cursor.execute("DELETE FROM veiculos WHERE id = %s", (id,))

        # 3. Commits it again to confirm the changes in the database. IT'S VERY IMPORTANT!
        conn.commit()

        # 4. Verifies if any row was actually deleted.
        # If cursor.rowcount == 0, it means that no vehicle was found with that ID.
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "Veículo não encontrado"}), 404

        # 5. Closes everything to avoid memory leaks.
        cursor.close()
        conn.close()

        # 6. Returns an succes message to the client.
        return jsonify({"message": "Veículo deletado com sucesso!"}), 200

    except Exception as e:
        # Secutity block to capture any error and print it in the terminal.
        print(f"Ocorreu um erro ao deletar: {e}")
        return jsonify({"error": str(e)}), 500