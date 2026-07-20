from flask import Blueprint, render_template

from app.services.relatorio_service import RelatorioService
from app.services.auth_service import login_required

configuracoes_bp = Blueprint(
    "configuracoes",
    __name__,
    url_prefix="/configuracoes"
)


@configuracoes_bp.route("/")
@login_required
def index():

    resumo = RelatorioService.resumo_geral()

    return render_template(
        "configuracoes/index.html",
        resumo=resumo
    )
