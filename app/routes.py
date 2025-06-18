from app import app, db
from flask import render_template, request, redirect, url_for
import sqlite3

from app.models import Usuario, Diario
from app.forms import UsuarioForm


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

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    form = UsuarioForm()
    context = {}
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('login'))
    
    return render_template("cadastro.html", context=context, form=form)


@app.route('/meuperfil')
def meuperfil():
    return render_template('meuperfil.html')

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/diario")
def diario():
    return render_template("diario.html")


@app.route('/salvar-diario', methods=['POST'])
#@login_required
def salvar_diario(): #usuario_id=current_user.id (colocar entre os parenteses quando resolver o login)
    try:
        # Uma nova entrada no diário
        nova_entrada = Diario()
        
        todos_os_campos = [
            # Emoções
            'feliz', 'triste', 'alteracao_humor', 'sensivel', 'raiva', 'irritavel',
            'ansiosa', 'falta_controle', 'indiferenca',
            # Mente
            'mente_confusa', 'calma', 'estresse', 'motivacao', 'criatividade',
            'bom_rendimento', 'preguica_desanimo', 'coracao_partido',
            # Sociabilidade
            'sociavel', 'introvertida', 'compreensiva', 'amorosa', 'conflituosa',
            # Lazer
            'ferias', 'encontro', 'ressaca', 'alcool', 'cigarro',
            # Sintomas Físicos
            'dor_cabeca','tensao_corporal', 'dor_corporal', 'insonia', 'queda_cabelo', 'taquicardia',
            'surto_acne', 'sem_apetite', 'alergia_dermatite', 'gripe', 'alteracao_hormonal', 'problemas_digestivos',
            # Comportamento do Parceiro
            'piadas_ofensivas', 'chantagem', 'mentira', 'dar_gelo', 'ciumes',
            'culpar', 'desqualificar', 'humilhar', 'xingamentos', 'ameacar',
            'proibir', 'destruir_bens', 'apertar', 'brincar_de_bater', 'beliscar',
            'empurrar', 'bater', 'chutar', 'confinar', 'ameacar_com_objetos',
            'ameacar_com_armas', 'ameacar_de_morte', 'obrigou_a_ter_relacoes_sexuais',
            'abuso_sexual', 'sufocar', 'feriu_animal', 'tentou_se_matar'
        ]
        
        for campo in todos_os_campos:
            if campo in request.form:
                setattr(nova_entrada, campo, True)
        
        # calculo
        nova_entrada.pontuacao = nova_entrada.calcular_pontuacao()
        
        # Salva
        db.session.add(nova_entrada)
        db.session.commit()
        
        # Redirecionamento pra pagina do diario
        return redirect(url_for('diario'))
    
    except Exception:
        db.session.rollback()
        return redirect(url_for('diario'))


@app.route('/ciclo')
def ciclo():
    return render_template('ciclo.html')