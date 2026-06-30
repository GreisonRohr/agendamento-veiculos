from flask import Blueprint, render_template

from app.services.dashboard_service import DashboardService

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/")
def index():

    return render_template(
        "dashboard.html",

        indicadores=DashboardService.indicadores(),

        agendamentos=DashboardService.proximos_agendamentos(),

        retornos=DashboardService.retornos_hoje(),

        manutencoes=DashboardService.manutencoes(),

        revisoes=DashboardService.proximas_revisoes()
    )