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