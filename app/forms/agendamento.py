from flask_wtf import FlaskForm

from wtforms import (
    SelectField,
    StringField,
    TextAreaField,
    DateField,
    TimeField,
    SubmitField,
)

from wtforms.validators import DataRequired


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

    motivo = TextAreaField("Motivo")

    data_saida = DateField(
        "Data da saída",
        validators=[DataRequired()]
    )

    hora_saida = TimeField(
        "Hora da saída",
        validators=[DataRequired()]
    )

    data_retorno = DateField(
        "Data do retorno",
        validators=[DataRequired()]
    )

    hora_retorno = TimeField(
        "Hora do retorno",
        validators=[DataRequired()]
    )

    observacoes = TextAreaField("Observações")

    submit = SubmitField("Salvar")