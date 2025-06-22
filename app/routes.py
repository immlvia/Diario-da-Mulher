from app import app, db
from flask import render_template, request, redirect, url_for, flash
import sqlite3
from app.models import Usuario
from app.forms import UsuarioForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required
from app.utils import formatar_data_atual
from app.diario_service import registrar_diario


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

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    form = UsuarioForm()
    context = {}
    if form.validate_on_submit():
        usuario = form.save()
        login_user(usuario, remember=True)
        return redirect(url_for('login'))
    
    return render_template("cadastro.html", context=context, form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = form.login()
        login_user(usuario, remember=True)
        return redirect(url_for('homepage'))
    
    return render_template("login.html", form=form)

@app.route("/sair")
def logout():
    logout_user()
    form = LoginForm()
    return render_template("login.html", form=form)

@app.route("/")
def homepage():
    if current_user.is_authenticated:
        return render_template("index.html")
    else:
        form = LoginForm()
        return render_template("login.html", form=form)

@app.route('/meuperfil')
def meuperfil():
    return render_template('meuperfil.html')

#@app.route("/<int:id>")
#def meuperfil(id):
#    obj = Usuario.query.get(id)
#    return render_template("meuperfil.html", obj=obj)

@app.route("/diario", methods=["GET"])
def diario():
    data_atual = formatar_data_atual()
    return render_template("diario.html", data_atual=data_atual)


@app.route('/ciclo')
def ciclo():
    return render_template('ciclo.html')

@app.route('/calendario')
def calendario():
    return render_template('calendario.html')

@app.route('/salvar-diario', methods=['POST'])
@login_required
def salvar_diario():
    try:
        # Registrar a entrada do diário usando o serviço
        registrar_diario(current_user.id, request.form)
        
        # Mensagem de sucesso
        flash('Seu diário foi registrado com sucesso!', 'success')
        
        # Redirecionamento para a página do diário
        return redirect(url_for("diario"))
    
    except Exception as e:
        # Tratar erros
        db.session.rollback()
        app.logger.error(f"Erro ao salvar diário: {e}")
        flash('Ocorreu um erro ao salvar seu diário. Por favor, tente novamente.', 'error')
        return redirect(url_for('diario'))