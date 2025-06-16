from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

from app import db
from app.models import Usuario

class UsuarioForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField ("Senha", validators=[DataRequired()])
    btnSubmit = SubmitField ("Enviar")

    def save(self):
        usuario = Usuario(
            nome = self.nome.data,
            email = self.email.data,
            senha = self.senha.data
        )

        db.session.add(usuario)
        db.session.commit()