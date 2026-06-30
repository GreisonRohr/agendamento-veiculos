from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
)

from app.forms import AgendamentoForm
from app.services.agendamento_service import AgendamentoService
from app.services.veiculo_service import VeiculoService

agendamentos_bp = Blueprint(
    "agendamentos",
    __name__,
    url_prefix="/agendamentos",
)


@agendamentos_bp.route("/")
def index():

    agendamentos = AgendamentoService.listar()

    return render_template(
        "agendamentos/index.html",
        agendamentos=agendamentos
    )


@agendamentos_bp.route("/novo", methods=["GET", "POST"])
def novo():

    form = AgendamentoForm()

    form.veiculo.choices = [
        (
            v.id,
            f"{v.placa} - {v.modelo}"
        )
        for v in VeiculoService.listar()
    ]

    if form.validate_on_submit():

        agendamento = AgendamentoService.criar(form)

        if agendamento is None:

            flash(
                "Este veículo já possui um agendamento nesse período.",
                "danger"
            )

            return render_template(
                "agendamentos/novo.html",
                form=form
            )

        flash(
            "Agendamento realizado com sucesso.",
            "success"
        )

        return redirect(
            url_for("agendamentos.index")
        )

    return render_template(
        "agendamentos/novo.html",
        form=form
    )

@agendamentos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    agendamento = AgendamentoService.buscar_por_id(id)

    form = AgendamentoForm(obj=agendamento)

    form.veiculo.choices = [
        (v.id, f"{v.placa} - {v.modelo}")
        for v in VeiculoService.listar()
    ]

    if form.validate_on_submit():

        atualizado = AgendamentoService.atualizar(id, form)

        if atualizado is None:

            flash(
                "Já existe um agendamento para este veículo nesse horário.",
                "danger"
            )

            return render_template(
                "agendamentos/editar.html",
                form=form
            )

        flash(
            "Agendamento atualizado com sucesso.",
            "success"
        )

        return redirect(
            url_for("agendamentos.index")
        )

    return render_template(
        "agendamentos/editar.html",
        form=form
    )

@agendamentos_bp.route("/excluir/<int:id>")
def excluir(id):

    AgendamentoService.excluir(id)

    flash(
        "Agendamento cancelado com sucesso.",
        "warning"
    )

    return redirect(
        url_for("agendamentos.index")
    )