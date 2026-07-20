from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
)

from app.forms import UsuarioForm
from app.services.usuario_service import UsuarioService
from app.services.auth_service import login_required, admin_required

usuarios_bp = Blueprint(
    "usuarios",
    __name__,
    url_prefix="/usuarios"
)


@usuarios_bp.route("/")
@login_required
@admin_required
def index():

    return render_template(
        "usuarios/index.html",
        usuarios=UsuarioService.listar()
    )


@usuarios_bp.route("/novo", methods=["GET", "POST"])
@login_required
@admin_required
def novo():

    form = UsuarioForm()

    if form.validate_on_submit():

        if UsuarioService.buscar_por_email(form.email.data):
            flash("Já existe um usuário com este e-mail.", "danger")
            return render_template("usuarios/novo.html", form=form)

        UsuarioService.criar(form)
        flash("Usuário criado com sucesso.", "success")
        return redirect(url_for("usuarios.index"))

    return render_template(
        "usuarios/novo.html",
        form=form
    )


@usuarios_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def editar(id):

    usuario = UsuarioService.buscar_por_id(id)
    form = UsuarioForm(obj=usuario)

    if form.validate_on_submit():

        email_existente = UsuarioService.buscar_por_email(form.email.data)
        if email_existente and email_existente.id != id:
            flash("Já existe um usuário com este e-mail.", "danger")
            return render_template("usuarios/editar.html", form=form, usuario=usuario)

        UsuarioService.atualizar(id, form)
        flash("Usuário atualizado com sucesso.", "success")
        return redirect(url_for("usuarios.index"))

    return render_template(
        "usuarios/editar.html",
        form=form,
        usuario=usuario
    )


@usuarios_bp.route("/excluir/<int:id>")
@login_required
@admin_required
def excluir(id):

    UsuarioService.excluir(id)
    flash("Usuário removido com sucesso.", "warning")

    return redirect(url_for("usuarios.index"))
