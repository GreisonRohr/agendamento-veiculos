from functools import wraps

from flask import session, redirect, url_for, flash

from app.extensions import db
from app.models import Usuario


class AuthService:

    @staticmethod
    def login(email, senha):
        """Autentica usuário e armazena na sessão."""
        usuario = Usuario.query.filter_by(
            email=email,
            ativo=True
        ).first()

        if usuario and usuario.verificar_senha(senha):
            session["usuario_id"] = usuario.id
            session["usuario_nome"] = usuario.nome
            session["is_admin"] = usuario.is_admin
            return usuario

        return None

    @staticmethod
    def logout():
        """Remove usuário da sessão."""
        session.pop("usuario_id", None)
        session.pop("usuario_nome", None)
        session.pop("is_admin", None)

    @staticmethod
    def usuario_atual():
        """Retorna o usuário logado ou None."""
        if "usuario_id" in session:
            return Usuario.query.get(session["usuario_id"])
        return None

    @staticmethod
    def esta_logado():
        return "usuario_id" in session

    @staticmethod
    def eh_admin():
        return session.get("is_admin", False)


def login_required(f):
    """Decorador: exige login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not AuthService.esta_logado():
            flash("Faça login para acessar esta página.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorador: exige ser administrador."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not AuthService.esta_logado():
            flash("Faça login para acessar esta página.", "warning")
            return redirect(url_for("auth.login"))
        if not AuthService.eh_admin():
            flash("Você não tem permissão para acessar esta página.", "danger")
            return redirect(url_for("dashboard.index"))
        return f(*args, **kwargs)
    return decorated_function
