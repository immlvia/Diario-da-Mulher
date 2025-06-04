# (Imports e outras configurações do Flask)
from flask import Flask, request, jsonify, render_template, send_from_directory
import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FOLDER = os.path.join(BASE_DIR, '..', 'frontend')
STATIC_FOLDER = os.path.join(BASE_DIR, '..', 'frontend')

app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)

DATABASE = os.path.join(BASE_DIR, 'database', 'database.db')
os.makedirs(os.path.join(BASE_DIR, 'database'), exist_ok=True)

# --- FUNÇÕES DE BANCO DE DADOS (coloque-as AQUI) ---

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(): # << A definição desta função precisa estar aqui
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diary_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_date TEXT NOT NULL,
            response_text TEXT NOT NULL,
            score INTEGER NOT NULL,
            level TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso!")

# --- LÓGICA DO VIOLÔMETRO (coloque-a AQUI) ---

def calculate_violometer_level(responses_scores):
    total_score = sum(responses_scores)
    if total_score >= 30:
        return "Nível de Perigo Extremo", "Procure ajuda imediatamente! Sua vida pode estar em risco."
    elif total_score >= 20:
        return "Nível de Alerta Alto", "Atenção! A situação pode escalar rapidamente. Busque apoio."
    elif total_score >= 10:
        return "Nível de Alerta Médio", "Fique atenta aos sinais. Converse com alguém de confiança."
    else:
        return "Nível de Alerta Baixo", "Observe o comportamento. Mantenha-se segura."

# --- ROTAS DA API (coloque-as AQUI) ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/diary', methods=['POST'])
def add_diary_entry():
    data = request.get_json()
    if not data or 'response_text' not in data or 'score' not in data:
        return jsonify({"error": "Dados inválidos. 'response_text' e 'score' são obrigatórios."}), 400

    response_text = data['response_text']
    score = data['score']
    entry_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_level, alert_message = calculate_violometer_level([score])

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO diary_entries (entry_date, response_text, score, level) VALUES (?, ?, ?, ?)",
            (entry_date, response_text, score, current_level)
        )
        conn.commit()
        conn.close()
        return jsonify({
            "message": "Registro adicionado com sucesso!",
            "entry": {
                "entry_date": entry_date,
                "response_text": response_text,
                "score": score,
                "level": current_level,
                "alert": alert_message
            }
        }), 201
    except Exception as e:
        print(f"Erro ao adicionar registro: {e}")
        return jsonify({"error": "Erro interno do servidor ao adicionar registro."}), 500

@app.route('/api/diary', methods=['GET'])
def get_diary_entries():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM diary_entries ORDER BY created_at DESC")
        entries = cursor.fetchall()
        conn.close()
        entries_list = [dict(entry) for entry in entries]
        return jsonify(entries_list), 200
    except Exception as e:
        print(f"Erro ao obter registros: {e}")
        return jsonify({"error": "Erro interno do servidor ao obter registros."}), 500

@app.route('/script.js')
def serve_script():
    return send_from_directory(app.static_folder, 'script.js')

@app.route('/style.css')
def serve_style():
    return send_from_directory(app.static_folder, 'style.css')


# --- EXECUÇÃO DA APLICAÇÃO ---
if __name__ == '__main__':
    # Aqui a função init_db() será chamada DEPOIS de ter sido definida
    init_db()
    app.run(debug=True)
    