from flask import Blueprint, render_template

from app.services.dashboard_service import DashboardService
from app.services.auth_service import login_required

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/")
@login_required
def index():

    return render_template(
        "dashboard.html",

        indicadores=DashboardService.indicadores(),

        agendamentos=DashboardService.proximos_agendamentos(),

        retornos=DashboardService.retornos_hoje(),

        manutencoes=DashboardService.manutencoes(),

        manutencoes_ativas=DashboardService.manutencoes_ativas(),

        revisoes=DashboardService.proximas_revisoes()
    )
