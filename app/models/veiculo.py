from app.extensions import db


class Veiculo(db.Model):
    __tablename__ = "veiculos"

    id = db.Column(db.Integer, primary_key=True)

    placa = db.Column(db.String(10), unique=True, nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    ano = db.Column(db.Integer)
    cor = db.Column(db.String(30))
    unidade = db.Column(db.String(100))
    km_atual = db.Column(db.Integer, default=0)

    status = db.Column(
        db.String(20),
        nullable=False,
        default="Disponível"
    )

    ultima_revisao = db.Column(db.Date)
    proxima_revisao = db.Column(db.Date)

    observacoes = db.Column(db.Text)

    ativo = db.Column(db.Boolean, default=True)

    agendamentos = db.relationship(
        "Agendamento",
        back_populates="veiculo",
        cascade="all, delete-orphan"
    )

    @property
    def badge_status(self):

        cores = {
            "Disponível": "success",
            "Em uso": "primary",
            "Manutenção": "danger",
            "Inativo": "secondary",
        }

        return cores.get(self.status, "secondary")

    def __repr__(self):
        return f"<Veiculo {self.placa}>"