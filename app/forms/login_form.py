from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Optional


class LoginForm(FlaskForm):

    email = StringField(
        "E-mail",
        validators=[DataRequired(), Email()]
    )

    senha = PasswordField(
        "Senha",
        validators=[DataRequired()]
    )

    submit = SubmitField("Entrar")
