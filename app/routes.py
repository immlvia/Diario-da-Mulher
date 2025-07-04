from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.models import Usuario, Diario
from app.forms import UsuarioForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required
from app.utils import formatar_data_atual
from app.diario_service import registrar_diario, obter_historico_diario, mapeamento_campos
from app.ciclo_service import calcular_dados_ciclo
from app.calendario_service import opcoes_legiveis, categorias_legiveis
from wtforms.validators import ValidationError
from app.forms import EditarContaForm
from datetime import date
from sqlalchemy import func



@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    form = UsuarioForm()
    context = {}
    if form.validate_on_submit():
        try:
            usuario = form.save()
            login_user(usuario, remember=True)
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('login'))
        except ValidationError as e:
            flash(str(e), 'error')
    return render_template("cadastro.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        usuario, status = form.login()

        if status == "email_incorreto":
            flash("Email não cadastrado no sistema", "error")
            return redirect(url_for('login'))
        elif status == "senha_incorreta":
            flash("Senha incorreta", "error")
            return redirect(url_for('login'))
        else:
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


@app.route("/diario", methods=["GET"])
def diario():
    data_atual = formatar_data_atual()
    return render_template("diario.html", data_atual=data_atual)


@app.route('/ciclo')
@login_required
def ciclo():
    #Chama a função pra obter a porcentagem
    porcentagem_ciclo = calcular_dados_ciclo(current_user.id)

    #Envia a porcentagem pro HTML
    return render_template('ciclo.html', porcentagem=porcentagem_ciclo)


@app.route('/calendario')
def calendario():
    usuario_id = current_user.id
    entradas = obter_historico_diario(usuario_id)
    return render_template("calendario.html", entradas=entradas, mapeamento_campos=mapeamento_campos, opcoes_legiveis=opcoes_legiveis, categorias_legiveis=categorias_legiveis)


@app.route('/salvar-diario', methods=['POST'])
@login_required
def salvar_diario():
    hoje = date.today()
    try:
        #Bloco para que so possa ter 1 registro por dia. Para mudar, comente ate a linha 107
        diario_de_hoje = Diario.query.filter(
           Diario.usuario_id == current_user.id,
           func.date(Diario.data) == hoje
        ).first()
        if diario_de_hoje:
           flash("Você ja realizou um registro hoje, faça um novo amanhã", 'error')
           return redirect(url_for('diario'))
        
        registrar_diario(current_user.id, request.form)
        flash('Seu diário foi registrado com sucesso!', 'success')
        return redirect(url_for("diario"))
    
    except Exception as e:
        #Tratar erros
        db.session.rollback()
        app.logger.error(f"Erro ao salvar diário: {e}")
        flash('Ocorreu um erro ao salvar seu diário. Por favor, tente novamente.', 'error')
        return redirect(url_for('diario'))



@app.route("/editar-conta", methods=["GET", "POST"])
@login_required
def editar_conta():
    form = EditarContaForm(usuario_atual=current_user)

    if form.validate_on_submit():
        form.salvar()
        flash("Dados atualizados com sucesso!", "success")
        return redirect(url_for("meuperfil"))

    # Pré-preenche no GET
    if request.method == "GET":
        form.nome.data = current_user.nome
        form.email.data = current_user.email

    return render_template("editar_conta.html", form=form)
