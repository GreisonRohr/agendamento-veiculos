from flask_wtf import FlaskForm
from wtforms.validators import Optional

from wtforms import (
    StringField,
    IntegerField,
    SelectField,
    TextAreaField,
    SubmitField,
    DateField
)
from wtforms.validators import DataRequired, Optional


class VeiculoForm(FlaskForm):

    placa = StringField(
        "Placa",
        validators=[DataRequired()]
    )

    marca = StringField(
        "Marca",
        validators=[DataRequired()]
    )

    modelo = StringField(
        "Modelo",
        validators=[DataRequired()]
    )

    ano = IntegerField("Ano")

    cor = StringField("Cor")

    unidade = StringField("Unidade")


    km_atual = IntegerField(
        "Quilometragem",
        validators=[Optional()]
    )

    status = SelectField(
        "Status",
        choices=[
            ("Disponível", "Disponível"),
            ("Em uso", "Em uso"),
            ("Manutenção", "Manutenção"),
            ("Inativo", "Inativo"),
        ],
    )

    ultima_revisao = DateField(
        "Última Revisão",
        validators=[Optional()],
        format="%Y-%m-%d"
    )

    proxima_revisao = DateField(
        "Próxima Revisão",
        validators=[Optional()],
        format="%Y-%m-%d"
    )

    observacoes = TextAreaField("Observações")

    submit = SubmitField("Salvar")