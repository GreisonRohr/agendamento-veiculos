from flask import Blueprint, render_template

from app.services.agenda_service import AgendaService

agenda_bp = Blueprint(
    "agenda",
    __name__,
    url_prefix="/agenda"
)


@agenda_bp.route("/")
def index():

    return render_template(
        "agenda/index.html",
        proximas_saidas=AgendaService.proximas_saidas(),
        retornos=AgendaService.retornos_hoje(),
        livres=AgendaService.veiculos_livres(),
        manutencoes=AgendaService.manutencoes()
    )