from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    StringField,
    TextAreaField,
    DateField,
    TimeField,
    SubmitField
)
from wtforms.validators import DataRequired, Optional


class AgendamentoForm(FlaskForm):

    veiculo = SelectField(
        "Veículo",
        coerce=int,
        validators=[DataRequired()]
    )

    motorista = StringField(
        "Motorista",
        validators=[DataRequired()]
    )

    destino = StringField(
        "Destino",
        validators=[DataRequired()]
    )

    motivo = TextAreaField(
        "Motivo",
        validators=[Optional()]
    )

    data_saida = DateField(
        "Data de Saída",
        validators=[DataRequired()]
    )

    hora_saida = TimeField(
        "Hora de Saída",
        validators=[DataRequired()]
    )

    data_retorno = DateField(
        "Data de Retorno",
        validators=[DataRequired()]
    )

    hora_retorno = TimeField(
        "Hora de Retorno",
        validators=[DataRequired()]
    )

    observacoes = TextAreaField(
        "Observações",
        validators=[Optional()]
    )

    submit = SubmitField("Salvar")
