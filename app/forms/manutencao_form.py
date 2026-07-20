from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    TextAreaField,
    DateField,
    DecimalField,
    SubmitField
)
from wtforms.validators import DataRequired, Optional, NumberRange


class ManutencaoForm(FlaskForm):

    veiculo = SelectField(
        "Veículo",
        coerce=int,
        validators=[DataRequired()]
    )

    tipo = SelectField(
        "Tipo de Manutenção",
        choices=[
            ("Preventiva", "Preventiva"),
            ("Corretiva", "Corretiva"),
            ("Revisão", "Revisão"),
            ("Pneus", "Pneus"),
            ("Outro", "Outro")
        ],
        validators=[DataRequired()]
    )

    descricao = TextAreaField(
        "Descrição",
        validators=[Optional()]
    )

    data_inicio = DateField(
        "Data de Início",
        validators=[DataRequired()]
    )

    data_fim = DateField(
        "Data de Término",
        validators=[Optional()]
    )

    custo = DecimalField(
        "Custo (R$)",
        places=2,
        validators=[Optional(), NumberRange(min=0)]
    )

    status = SelectField(
        "Status",
        choices=[
            ("Em andamento", "Em andamento"),
            ("Concluída", "Concluída"),
            ("Cancelada", "Cancelada")
        ],
        default="Em andamento"
    )

    oficina = StringField(
        "Oficina / Responsável",
        validators=[Optional()]
    )

    submit = SubmitField("Salvar")
