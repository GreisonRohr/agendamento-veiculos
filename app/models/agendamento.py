from datetime import datetime

from app.extensions import db


class Agendamento(db.Model):
    __tablename__ = "agendamentos"

    id = db.Column(db.Integer, primary_key=True)

    veiculo_id = db.Column(
        db.Integer,
        db.ForeignKey("veiculos.id"),
        nullable=False
    )

    usuario_id = db.Column(
        db.Integer,
        nullable=True
    )

    motorista = db.Column(
        db.String(100),
        nullable=False
    )

    destino = db.Column(
        db.String(200),
        nullable=False
    )

    motivo = db.Column(db.Text)

    data_saida = db.Column(
        db.Date,
        nullable=False
    )

    hora_saida = db.Column(
        db.Time,
        nullable=False
    )

    data_retorno = db.Column(
        db.Date,
        nullable=False
    )

    hora_retorno = db.Column(
        db.Time,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Agendado"
    )

    observacoes = db.Column(db.Text)

    criado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    veiculo = db.relationship(
        "Veiculo",
        back_populates="agendamentos"
    )

    def __repr__(self):
        return f"<Agendamento {self.id}>"
