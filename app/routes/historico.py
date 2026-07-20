from flask import (
    Blueprint,
    render_template,
    request,
)

from app.forms import HistoricoForm
from app.services.historico_service import HistoricoService
from app.services.veiculo_service import VeiculoService
from app.services.auth_service import login_required

historico_bp = Blueprint(
    "historico",
    __name__,
    url_prefix="/historico"
)


@historico_bp.route("/", methods=["GET", "POST"])
@login_required
def index():

    form = HistoricoForm()

    # Preenche o select de veículos
    form.veiculo.choices = [(0, "Todos")] + [
        (v.id, f"{v.placa} - {v.modelo}")
        for v in VeiculoService.listar()
    ]

    resultados = []

    if form.validate_on_submit():

        resultados = HistoricoService.buscar(
            data_inicio=form.data_inicio.data,
            data_fim=form.data_fim.data,
            veiculo_id=form.veiculo.data if form.veiculo.data != 0 else None,
            motorista=form.motorista.data,
            status=form.status.data if form.status.data else None
        )

    return render_template(
        "historico/index.html",
        form=form,
        resultados=resultados
    )


@historico_bp.route("/exportar", methods=["POST"])
@login_required
def exportar():

    form = HistoricoForm()
    form.veiculo.choices = [(0, "Todos")] + [
        (v.id, f"{v.placa} - {v.modelo}")
        for v in VeiculoService.listar()
    ]

    if form.validate_on_submit():

        resultados = HistoricoService.buscar(
            data_inicio=form.data_inicio.data,
            data_fim=form.data_fim.data,
            veiculo_id=form.veiculo.data if form.veiculo.data != 0 else None,
            motorista=form.motorista.data,
            status=form.status.data if form.status.data else None
        )

        return HistoricoService.exportar_csv(resultados)

    return render_template(
        "historico/index.html",
        form=form,
        resultados=[]
    )
