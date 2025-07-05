from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from app import db, bcrypt
from app.models import Usuario
from sqlalchemy.exc import IntegrityError

class UsuarioForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField ("Senha", validators=[DataRequired()])
    btnSubmit = SubmitField ("Cadastrar")

    def validate_email(self, email):
        if Usuario.query.filter_by(email=email.data).first():
           raise ValidationError('Usuário já cadastrado com esse Email.')

    def save(self):
        try:
            senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))

            usuario = Usuario(
                nome = self.nome.data,
                email = self.email.data,
                senha = senha
        )

            db.session.add(usuario)
            db.session.commit()
            return usuario
        except IntegrityError:
            db.session.rollback()
            raise ValidationError('Este email já está cadastrado.')



class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    btnSubmit = SubmitField("Entrar")

    def login(self):
        usuario = Usuario.query.filter_by(email=self.email.data).first()
        if usuario is None:
            return None, "email_incorreto"
        if not bcrypt.check_password_hash(usuario.senha, self.senha.data.encode('utf-8')):
            return None, "senha_incorreta"
        return usuario, "sucesso"
        
class EditarContaForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
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
        



