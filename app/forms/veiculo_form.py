from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    SelectField,
    TextAreaField,
    DateField,
    SubmitField
)
from wtforms.validators import DataRequired, Optional, NumberRange


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

    ano = IntegerField(
        "Ano",
        validators=[Optional(), NumberRange(min=1900, max=2100)]
    )

    cor = StringField(
        "Cor",
        validators=[Optional()]
    )

    unidade = StringField(
        "Unidade",
        validators=[Optional()]
    )

    km_atual = IntegerField(
        "Quilometragem Atual",
        validators=[Optional(), NumberRange(min=0)]
    )

    status = SelectField(
        "Status",
        choices=[
            ("Disponível", "Disponível"),
            ("Em uso", "Em uso"),
            ("Manutenção", "Manutenção"),
            ("Inativo", "Inativo"),
        ],
        default="Disponível"
    )

    ultima_revisao = DateField(
        "Última Revisão",
        validators=[Optional()]
    )

    proxima_revisao = DateField(
        "Próxima Revisão",
        validators=[Optional()]
    )

    observacoes = TextAreaField(
        "Observações",
        validators=[Optional()]
    )

    submit = SubmitField("Salvar")
