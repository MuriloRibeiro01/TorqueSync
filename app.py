# Importar o 'wraps'
from functools import wraps

# Importa o Flask e outras feramentas que serão úteis
from flask import Flask, jsonify, request

from flask_cors import CORS # Importa o CORS

# Importa o conecetor do MySQL
import mysql.connector

# Aqui é criado um Decorator
def validacao_veiculo_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        # Primeiro ele pega os dados
        dados = request.get_json()

        # Segundo ele faz a validação
        if not dados or 'placa' not in dados or 'modelo' not in dados:
            return jsonify({"error": "Dados incompletos. Placa e modelo são obrigatórios"}), 400  # 400 = Bad Request

        # Terceiro, se tudo estiver OK, ele continua para a rota original
        return f(dados = dados, *args, **kwargs)
    return decorated_function

# Cria a instância da nossa aplicação
app = Flask(__name__)
CORS(app) # Inicializa o CORS com a aplicação

# Configuração da coneção com o Banco de Dados
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '!Itadaki08'
app.config['MYSQL_DB'] = 'database_torquesync'

# Função para conectar com o database
def get_db_connection():
    conn = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )
    return conn


# Rota para listar os veículos (VERSÃO DE DEPURAÇÃO)
@app.route('/api/veiculos', methods=['GET'])
def get_veiculos():
    print("\n--- Rota /api/veiculos foi chamada! ---")

    conn = None  # Apenas para garantir que a variável exista
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
        # Este bloco vai pegar qualquer erro e nos mostrar no terminal!
        print("\n!!!!!! OCORREU UMA EXCEÇÃO NO BLOCO TRY !!!!!!")
        print(f"TIPO DO ERRO: {type(e)}")
        print(f"MENSAGEM DO ERRO: {e}\n")

        # Bloco de segurança para garantir que a conexão seja fechada em caso de erro
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("Conexão de emergência com o banco foi fechada.")

        # Retorna o erro para o frontend, mas o print no terminal é o mais importante
        return jsonify({'error': str(e)}), 500


# Rota para Buscar um específico (Ex: buscar só o carro com ID = 1)
@app.route('/api/veiculos/<int:id>', methods=['GET'])
def get_veiculo_por_id(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT * FROM veiculos WHERE id = %s', (id,))

        veiculo = cursor.fetchone() # fetchone() pega apenas um resultado

        cursor.close()
        conn.close()

        if veiculo:
            return jsonify(veiculo), 200
        else:
            return jsonify({"error": "Veículo não encontrado"}), 404 # 404 é o código para "não encontrado"

    except Exception as e:
        return jsonify({'error': str(e)}), 500




# Rota para criar um novo (Ex: adicionar um novo carro no database)
@app.route('/api/veiculos', methods=['POST'])
@validacao_veiculo_required
def criar_veiculo(dados):

    # Extrai os dados do JSON.
    placa = dados['placa']
    modelo = dados['modelo']
    ano = dados.get('ano') # o .get() vai ser mais seguro porque retorna None se a chave não existir.
    cor = dados.get('cor')
    quilometragem = dados.get('quilometragem')
    status = dados.get('status', 'Disponível') # Seta o valor como 'Disponível', já que um carro que acabou de chegar não vai estar alugado logo de cara.

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Query pra inserir o novo veículo.
        query = """
            INSERT INTO veiculos (placa, modelo, ano, cor, quilometragem, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        # Executa a query com os dados em uma tupla
        cursor.execute(query, (placa, modelo, ano, cor, quilometragem, status))

        # Pega o ID do veículo que foi criado
        novo_veiculo_id = cursor.lastrowid # Last Row ID

        # Isso confirma a transação
        conn.commit()

        cursor.close()
        conn.close()

        # Agora ele vai retornar o objeto em si
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

    except mysql.connector.Error as erro:
        # Trata os erros específicos do MySQL
        return jsonify({"error": str(erro)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Rota para Atualizar um existente (Ex: mudar o status de um carro)
@app.route('/api/veiculos/<int:id>', methods=['PUT'])
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

        # Query para atualizar o veiculo com um ID específico
        query = """
            UPDATE veiculos 
            SET placa = %s, modelo = %s, ano = %s, cor = %s, quilometragem = %s, status = %s
            WHERE id = %s
        """

        # Executa a query com os dados em uma tupla
        cursor.execute(query, (placa, modelo, ano, cor, quilometragem, status, id))

        conn.commit()

        # Verifica se alguma linha foi realmente atualizada
        if cursor.rowcount == 0:
            return jsonify({"error": "Veículo não encontrado"}), 404

        cursor.close()
        conn.close()

        # Aqui ele retorna uma reposta de sucesso
        return jsonify({"message": "Veículo atualizado com sucesso!"}), 200 # 200 = OK

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Rota para Deletar um (VERSÃO FINAL)
@app.route('/api/veiculos/<int:id>', methods=['DELETE'])
def deletar_veiculo(id):
    try:
        # 1. Abre a conexão com o banco, como já conhecemos.
        conn = get_db_connection()
        cursor = conn.cursor()

        # 2. Executamos o comando SQL DELETE para a ID específica.
        # Note a vírgula mágica em (id,) para criar a tupla e garantir segurança!
        cursor.execute("DELETE FROM veiculos WHERE id = %s", (id,))

        # 3. conn.commit() é CRUCIAL. Sem ele, a alteração fica 'pendente'
        # e nunca é salva de verdade no banco de dados.
        conn.commit()

        # 4. Verificamos se alguma linha foi de fato deletada.
        # Se cursor.rowcount for 0, significa que não encontramos nenhum veículo com aquele ID.
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "Veículo não encontrado"}), 404

        # 5. Fecha tudo para liberar recursos.
        cursor.close()
        conn.close()

        # 6. Retorna uma mensagem de sucesso para o cliente.
        return jsonify({"message": "Veículo deletado com sucesso!"}), 200

    except Exception as e:
        # Nosso bloco de segurança para capturar qualquer erro inesperado.
        print(f"Ocorreu um erro ao deletar: {e}")
        return jsonify({"error": str(e)}), 500

# Linha para rodar a aplicação em modo de desenvolvimento
if __name__ == '__main__':
    app.run(debug=True)

# Adicionar número do ID dos veículos
# Ao apagar um dos veículos, automaticamente transformar o próximo veículo naquele ID qual foi apagado.