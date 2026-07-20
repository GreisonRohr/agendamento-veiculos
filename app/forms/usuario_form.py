from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Optional


class UsuarioForm(FlaskForm):

    nome = StringField(
        "Nome",
        validators=[DataRequired()]
    )

    email = StringField(
        "E-mail",
        validators=[DataRequired(), Email()]
    )

    senha = PasswordField(
        "Senha",
        validators=[Optional()]
    )

    confirmar_senha = PasswordField(
        "Confirmar Senha",
        validators=[EqualTo("senha", message="As senhas devem coincidir.")]
    )

    is_admin = BooleanField(
        "Administrador"
    )

    submit = SubmitField("Salvar")
