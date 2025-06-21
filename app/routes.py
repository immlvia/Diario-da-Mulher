from app import app, db
from datetime import date
from flask import render_template, request, redirect, url_for
import sqlite3

from app.models import Diario, Usuario
from app.forms import UsuarioForm, LoginForm
from flask_login import login_user, logout_user, current_user


def conectar_db():
    conectar = sqlite3.connect()
    return conectar


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
    print(current_user.is_authenticated)
    return render_template("index.html")

@app.route('/meuperfil')
def meuperfil():
    return render_template('meuperfil.html')

#@app.route("/<int:id>")
#def meuperfil(id):
#    obj = Usuario.query.get(id)
#    return render_template("meuperfil.html", obj=obj)

@app.route("/diario")
def diario():
    usuario_id_atual = current_user.id 
    hoje = date.today()
    
    entrada_existente = Diario.query.filter_by(
        usuario_id=usuario_id_atual, 
        data_criacao=hoje
    ).first()

    if entrada_existente:
    #Se tiver registro do banco de dados que ja preencheou o diario hoje, a entrada é negada) e
    # redireciona para "calendario". colocar uma mensagem depois
        return redirect(url_for('calendario.html'))


    return render_template("diario.html")


@app.route('/ciclo')
def ciclo():
    return render_template('ciclo.html')


@app.route('/salvar-diario', methods=['POST'])
#@login_required
def salvar_diario():

    try:
        #Usuaria fez o "diario" hoje:
        dia_de_hoje = Diario(usuario_id=None) #current_user.id, modificar depois
        
        #Botões para html
        todos_os_campos = [
            # Emoções
            'feliz', 'triste', 'alteracao_humor', 'sensivel', 'raiva', 'irritavel',
            'ansiosa', 'falta_controle', 'indiferenca',
            
            # Mente
            'mente_confusa', 'calma', 'estresse', 'motivacao', 'criatividade',
            'bom_rendimento', 'preguica_desanimo',
            
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
            'proibir', 'destruir_bens', 'apertar', 'brincar_bater', 'beliscar',
            'empurrar', 'bater', 'chutar', 'confinar', 'ameacar_objetos',
            'ameacar_armas', 'ameacar_morte', 'obrigou_relacao_sexual',
            'abuso_sexual', 'sufocar', 'feriu_animal', 'tentou_se_matar'
        ]
        
        for campo in todos_os_campos:
            if campo in request.form:
                setattr(dia_de_hoje, campo, True)
        
        #Calcular Pontuação
        dia_de_hoje.pontuacao_total = dia_de_hoje.calcular_pontuacao()
        
        #Salvar pontuação no banco de dados
        db.session.add(dia_de_hoje)
        db.session.commit()
        
        # Redirecionamento pra pagina do index do site
        redirect(url_for("index"))
    
    except Exception:
        #tratar erros
        db.session.rollback()
        return redirect(url_for('index'))

    with app.app_context():
        #pra criar as colunas no banco de dados
        db.create_all()
        print("Tabelas criadas com sucesso.")


@app.route('/calendario')
def calendario():
    return render_template('calendario.html')