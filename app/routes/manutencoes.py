from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
)

from app.forms import ManutencaoForm
from app.services.manutencao_service import ManutencaoService
from app.services.veiculo_service import VeiculoService
from app.services.auth_service import login_required, admin_required

manutencoes_bp = Blueprint(
    "manutencoes",
    __name__,
    url_prefix="/manutencoes"
)


@manutencoes_bp.route("/")
@login_required
def index():

    manutencoes = ManutencaoService.listar()

    return render_template(
        "manutencoes/index.html",
        manutencoes=manutencoes
    )


@manutencoes_bp.route("/novo", methods=["GET", "POST"])
@admin_required
def novo():

    form = ManutencaoForm()

    form.veiculo.choices = [
        (v.id, f"{v.placa} - {v.modelo}")
        for v in VeiculoService.listar()
    ]

    if form.validate_on_submit():

        ManutencaoService.criar(form)

        flash(
            "Manutenção registrada com sucesso.",
            "success"
        )

        return redirect(
            url_for("manutencoes.index")
        )

    return render_template(
        "manutencoes/novo.html",
        form=form
    )


@manutencoes_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@admin_required
def editar(id):

    manutencao = ManutencaoService.buscar_por_id(id)

    form = ManutencaoForm(obj=manutencao)

    form.veiculo.choices = [
        (v.id, f"{v.placa} - {v.modelo}")
        for v in VeiculoService.listar()
    ]

    if form.validate_on_submit():

        ManutencaoService.atualizar(id, form)

        flash(
            "Manutenção atualizada com sucesso.",
            "success"
        )

        return redirect(
            url_for("manutencoes.index")
        )

    return render_template(
        "manutencoes/editar.html",
        form=form,
        manutencao=manutencao
    )


@manutencoes_bp.route("/excluir/<int:id>")
@admin_required
def excluir(id):

    ManutencaoService.excluir(id)

    flash(
        "Manutenção removida com sucesso.",
        "warning"
    )

    return redirect(
        url_for("manutencoes.index")
    )
