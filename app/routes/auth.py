from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
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

        print(f"Tentativa de login: {form.email.data}")

        usuario = AuthService.login(
            form.email.data,
            form.senha.data
        )

        if usuario:
            print(f"Login OK: {usuario.nome}")
            flash(f"Bem-vindo, {usuario.nome}!", "success")
            return redirect(url_for("dashboard.index"))
        else:
            print(f"Login falhou: {form.email.data}")
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


@auth_bp.route("/debug")
def debug():
    """Mostra usuários no banco para diagnóstico."""
    from app.models import Usuario
    try:
        usuarios = Usuario.query.all()
        resultado = []
        for u in usuarios:
            resultado.append({
                "id": u.id,
                "nome": u.nome,
                "email": u.email,
                "is_admin": u.is_admin,
                "ativo": u.ativo
            })
        return jsonify({"usuarios": resultado, "total": len(resultado)})
    except Exception as e:
        return jsonify({"erro": str(e)})


@auth_bp.route("/setup")
def setup():
    """Rota para criar usuários manualmente."""
    try:
        from app.extensions import db
        from app.models import Usuario

        # Cria admin
        admin = Usuario.query.filter_by(email="admin@garagemlab.com").first()
        if not admin:
            admin = Usuario(
                nome="Administrador",
                email="admin@garagemlab.com",
                is_admin=True,
                ativo=True
            )
            admin.set_senha("admin123")
            db.session.add(admin)
            db.session.commit()

        # Cria usuário comum
        usuario = Usuario.query.filter_by(email="usuario@garagemlab.com").first()
        if not usuario:
            usuario = Usuario(
                nome="Usuário Comum",
                email="usuario@garagemlab.com",
                is_admin=False,
                ativo=True
            )
            usuario.set_senha("usuario123")
            db.session.add(usuario)
            db.session.commit()

        return jsonify({"status": "ok", "mensagem": "Usuários criados/verificados"})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)})
