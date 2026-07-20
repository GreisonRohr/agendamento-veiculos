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
from app.services.auth_service import login_required, admin_required

agendamentos_bp = Blueprint(
    "agendamentos",
    __name__,
    url_prefix="/agendamentos",
)


@agendamentos_bp.route("/")
@login_required
def index():

    agendamentos = AgendamentoService.listar()

    return render_template(
        "agendamentos/index.html",
        agendamentos=agendamentos
    )


@agendamentos_bp.route("/exportar")
@login_required
def exportar():
    """Exporta agendamentos para CSV."""
    return AgendamentoService.exportar_csv()


@agendamentos_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():

    form = AgendamentoForm()

    form.veiculo.choices = [
        (
            v.id,
            f"{v.placa} - {v.modelo}"
        )
        for v in VeiculoService.listar_disponiveis_para_agendamento()
    ]

    if form.validate_on_submit():

        agendamento = AgendamentoService.criar(form)

        if isinstance(agendamento, dict) and "erro" in agendamento:
            erro = agendamento["erro"]
            if erro == "conflito":
                flash(
                    "Este veículo já possui um agendamento nesse período.",
                    "danger"
                )
            else:
                flash(erro, "danger")

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
@login_required
def editar(id):

    agendamento = AgendamentoService.buscar_por_id(id)

    # Verifica permissão
    if not AgendamentoService.pode_editar(id):
        flash("Você não tem permissão para editar este agendamento.", "danger")
        return redirect(url_for("agendamentos.index"))

    form = AgendamentoForm(obj=agendamento)

    # Lista veículos disponíveis + o veículo atual do agendamento
    veiculos_disponiveis = VeiculoService.listar_disponiveis_para_agendamento()
    veiculo_atual = VeiculoService.buscar_por_id(agendamento.veiculo_id)

    veiculos_choices = []
    ids_adicionados = set()

    for v in veiculos_disponiveis:
        veiculos_choices.append((v.id, f"{v.placa} - {v.modelo}"))
        ids_adicionados.add(v.id)

    # Mantém o veículo atual na lista mesmo se não estiver disponível
    if veiculo_atual and veiculo_atual.id not in ids_adicionados:
        veiculos_choices.append((veiculo_atual.id, f"{veiculo_atual.placa} - {veiculo_atual.modelo} (indisponível)"))

    form.veiculo.choices = veiculos_choices

    if form.validate_on_submit():

        atualizado = AgendamentoService.atualizar(id, form)

        if isinstance(atualizado, dict) and "erro" in atualizado:
            erro = atualizado["erro"]
            if erro == "conflito":
                flash(
                    "Já existe um agendamento para este veículo nesse horário.",
                    "danger"
                )
            else:
                flash(erro, "danger")

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
@login_required
def excluir(id):

    # Verifica permissão
    if not AgendamentoService.pode_editar(id):
        flash("Você não tem permissão para cancelar este agendamento.", "danger")
        return redirect(url_for("agendamentos.index"))

    AgendamentoService.excluir(id)

    flash(
        "Agendamento cancelado com sucesso.",
        "warning"
    )

    return redirect(
        url_for("agendamentos.index")
    )
