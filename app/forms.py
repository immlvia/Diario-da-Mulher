from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

from app import db, bcrypt
from app.models import Usuario

class UsuarioForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField ("Senha", validators=[DataRequired()])
    btnSubmit = SubmitField ("Cadastrar")

    def validate_email(self, email):
        if Usuario.query.filter_by(email=email.data).first():
            return ValidationError('Usuário já cadastrado com esse Email.')

    def save(self):
        senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))

        usuario = Usuario(
            nome = self.nome.data,
            email = self.email.data,
            senha = senha
        )

        db.session.add(usuario)
        db.session.commit()
        return usuario

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    btnSubmit = SubmitField("Entrar")

    def login(self):
        usuario = Usuario.query.filter_by(email=self.email.data).first()
        if usuario:
            if bcrypt.check_password_hash(usuario.senha, self.senha.data.encode('utf-8')):
                return usuario
            else:
                raise Exception('Senha incorreta.')
        else:
            raise Exception('Usuário não cadastrado.')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from app import db, bcrypt
from app.models import Usuario

class EditarContaForm(FlaskForm):
    email = StringField("Novo Email", validators=[DataRequired(), Email()])
    senha_atual = PasswordField("Senha Atual", validators=[DataRequired()])
    nova_senha = PasswordField("Nova Senha", validators=[DataRequired()])
    btnSubmit = SubmitField("Salvar Alterações")

    def __init__(self, usuario_atual, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario_atual = usuario_atual

    def validate_email(self, field):
        if field.data != self.usuario_atual.email:
            if Usuario.query.filter_by(email=field.data).first():
                raise ValidationError("Este email já está em uso.")

    def validate_senha_atual(self, field):
        if not bcrypt.check_password_hash(self.usuario_atual.senha, field.data.encode('utf-8')):
            raise ValidationError("Senha atual incorreta.")

    def salvar(self):
        self.usuario_atual.email = self.email.data
        self.usuario_atual.senha = bcrypt.generate_password_hash(self.nova_senha.data.encode('utf-8'))
        db.session.commit()
