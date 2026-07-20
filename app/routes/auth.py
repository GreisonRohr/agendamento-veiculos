from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    session,
)

from app.forms import LoginForm
from app.services.auth_service import AuthService

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    # Se já estiver logado, redireciona
    if AuthService.esta_logado():
        return redirect(url_for("dashboard.index"))

    form = LoginForm()

    if form.validate_on_submit():

        usuario = AuthService.login(
            form.email.data,
            form.senha.data
        )

        if usuario:
            flash(f"Bem-vindo, {usuario.nome}!", "success")
            return redirect(url_for("dashboard.index"))
        else:
            flash("E-mail ou senha incorretos.", "danger")

    return render_template(
        "auth/login.html",
        form=form
    )


@auth_bp.route("/logout")
def logout():

    AuthService.logout()
    flash("Você saiu do sistema.", "info")

    return redirect(url_for("auth.login"))
