# (Imports e outras configurações do Flask)
from flask import Flask
from flask import render_template
import sqlite3

app = Flask(__name__)


def conectar_db():
    conectar = sqlite3.connect()
    return conectar


def criar_tabela():
    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute ('''
                   CREAT TABLE IF NOT EXISTS usuarios (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome TEXT NOT NULL,
                   idade INTEGER)
                   ''')
# rotas 
@app.route("/")
def homepage():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
