from datetime import datetime

from app.extensions import db


class Manutencao(db.Model):
    __tablename__ = "manutencoes"

    id = db.Column(db.Integer, primary_key=True)

    veiculo_id = db.Column(
        db.Integer,
        db.ForeignKey("veiculos.id"),
        nullable=False
    )

    tipo = db.Column(
        db.String(50),
        nullable=False
    )

    descricao = db.Column(db.Text)

    data_inicio = db.Column(
        db.Date,
        nullable=False
    )

    data_fim = db.Column(db.Date)

    custo = db.Column(
        db.Numeric(10, 2),
        default=0
    )

    status = db.Column(
        db.String(20),
        default="Em andamento"
    )

    oficina = db.Column(db.String(100))

    criado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    veiculo = db.relationship(
        "Veiculo",
        backref="manutencoes"
    )

    def __repr__(self):
        return f"<Manutencao {self.id} - {self.veiculo.placa if self.veiculo else 'N/A'}>"
