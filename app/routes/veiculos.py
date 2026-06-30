from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
)

from app.forms import VeiculoForm
from app.services.veiculo_service import VeiculoService

veiculos_bp = Blueprint(
    "veiculos",
    __name__,
    url_prefix="/veiculos",
)


@veiculos_bp.route("/")
def index():

    return render_template(
        "veiculos/index.html",
        veiculos=VeiculoService.listar(),
    )


@veiculos_bp.route("/novo", methods=["GET", "POST"])
def novo():

    form = VeiculoForm()

    if form.validate_on_submit():

        print("Placa digitada:", form.placa.data)

        veiculo_inativo = VeiculoService.buscar_por_placa_inativa(
            form.placa.data
        )

        print("Veículo inativo:", veiculo_inativo)

        # Verifica se existe veículo INATIVO
        veiculo_inativo = VeiculoService.buscar_por_placa_inativa(
            form.placa.data
        )

        if veiculo_inativo:

            return render_template(
                "veiculos/novo.html",
                form=form,
                veiculo_inativo=veiculo_inativo,
                mostrar_modal=True
            )

        # Verifica se existe veículo ATIVO
        if VeiculoService.buscar_por_placa(
            form.placa.data
        ):

            flash(
                "Já existe um veículo com essa placa.",
                "danger"
            )

            return render_template(
                "veiculos/novo.html",
                form=form,
                mostrar_modal=False
            )

        VeiculoService.criar(form)

        flash(
            "Veículo cadastrado com sucesso!",
            "success"
        )

        return redirect(
            url_for("veiculos.index")
        )

    return render_template(
        "veiculos/novo.html",
        form=form,
        mostrar_modal=False
    )



@veiculos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    veiculo = VeiculoService.buscar_por_id(id)

    form = VeiculoForm(obj=veiculo)

    if form.validate_on_submit():

        placa_existente = VeiculoService.buscar_por_placa(
            form.placa.data
        )

        if placa_existente and placa_existente.id != id:

            flash(
                "Já existe um veículo com essa placa.",
                "danger"
            )

            return render_template(
                "veiculos/editar.html",
                form=form
            )

        VeiculoService.atualizar(id, form)

        flash(
            "Veículo atualizado com sucesso.",
            "success"
        )

        return redirect(
            url_for("veiculos.index")
        )

    return render_template(
        "veiculos/editar.html",
        form=form
    )

@veiculos_bp.route("/excluir/<int:id>")
def excluir(id):

    VeiculoService.excluir(id)

    flash(
        "Veículo removido com sucesso.",
        "warning"
    )

    return redirect(
        url_for("veiculos.index")
    ) 


@veiculos_bp.route("/reativar/<int:id>", methods=["POST"])
def reativar(id):

    form = VeiculoForm()

    if form.validate_on_submit():

        VeiculoService.reativar(id, form)

        flash(
            "Veículo reativado com sucesso.",
            "success"
        )

        return redirect(
            url_for("veiculos.index")
        )

    flash(
        "Não foi possível reativar o veículo.",
        "danger"
    )

    return redirect(
        url_for("veiculos.novo")
    )