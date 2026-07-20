from flask import Blueprint, render_template

from app.services.relatorio_service import RelatorioService
from app.services.auth_service import login_required

relatorios_bp = Blueprint(
    "relatorios",
    __name__,
    url_prefix="/relatorios"
)


@relatorios_bp.route("/")
@login_required
def index():

    return render_template(
        "relatorios/index.html",
        resumo=RelatorioService.resumo_geral(),
        utilizacao=RelatorioService.utilizacao_frota()
    )
