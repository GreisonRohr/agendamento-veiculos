from flask import Blueprint

manutencoes_bp = Blueprint(
    "manutencoes",
    __name__,
    url_prefix="/manutencoes"
)


@manutencoes_bp.route("/")
def index():
    return "Módulo de Manutenções"