from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import uuid

def get_db():
    conn = sqlite3.connect('tarefas.db')
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
                CREATE TABLE IF NOT EXISTS tarefas (
                id TEXT PRIMARY KEY,
                titulo TEXT NOT NULL,
                descricao TEXT,
                concluida INTEGER NOT NULL);
                     ''')
init_db()

app = Flask(__name__)
CORS(app)

@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    with get_db() as conn:
        tarefas = conn.execute('SELECT * FROM tarefas').fetchall()
        return jsonify([dict(tarefa) for tarefa in tarefas]), 200
    
@app.route('/tarefas', methods=['POST'])
def adicionar_tarefa():
    data = request.get_json()
    if not data or not data.get('titulo'):
        return jsonify({'erro': 'Título é obrigatório'}), 400
    
    tarefa = {
        'id': str(uuid.uuid4()),
        'titulo':data['titulo'],
        'descricao':data.get('descricao',''),
        'concluida':0
    }

    with get_db() as conn:
        conn.execute('''
            INSERT INTO tarefas (id, titulo, descricao, concluida)
            VALUES (?,?,?,?)

''', (
    tarefa['id'],
    tarefa['titulo'],
    tarefa['descricao'],
    tarefa['concluida']
))
    conn.commit()

    return jsonify(tarefa), 201


app.run(debug=True, host='0.0.0.0', port=5000)