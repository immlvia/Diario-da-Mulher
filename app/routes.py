from flask import render_template, request, redirect, url_for
import sqlite3
from app import app


def conectar_db():
    conectar = sqlite3.connect()
    return conectar


def criar_tabela():
    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute ('''
                   CREAT TABLE IF NOT EXISTS usuarios (
                   id INTEGER PRIMARY KEY      AUTOINCREMENT,
                   nome TEXT NOT NULL,
                   idade INTEGER)
                   ''')
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")
        # lógica de autenticação
        if usuario == "admin" and senha == "1234":
            return redirect(url_for("homepage"))
        else:
            return render_template("login.html", erro="Usuário ou senha inválidos.")
    return render_template("login.html")

@app.route("/cadastro/")
def cadastro():
    return render_template("cadastro.html")

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/diario/")
def diario():
    return render_template("diario.html")