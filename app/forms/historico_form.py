from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    StringField,
    DateField,
    SubmitField
)
from wtforms.validators import Optional


class HistoricoForm(FlaskForm):

    data_inicio = DateField(
        "Data Início",
        validators=[Optional()]
    )

    data_fim = DateField(
        "Data Fim",
        validators=[Optional()]
    )

    veiculo = SelectField(
        "Veículo",
        coerce=int,
        validators=[Optional()]
    )

    motorista = StringField(
        "Motorista",
        validators=[Optional()]
    )

    status = SelectField(
        "Status",
        choices=[
            ("", "Todos"),
            ("Agendado", "Agendado"),
            ("Em andamento", "Em andamento"),
            ("Finalizado", "Finalizado"),
            ("Cancelado", "Cancelado")
        ],
        validators=[Optional()]
    )

    submit = SubmitField("Buscar")
