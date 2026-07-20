from app.extensions import db
from app.models import Usuario


class UsuarioService:

    @staticmethod
    def listar():
        return (
            Usuario.query
            .filter_by(ativo=True)
            .order_by(Usuario.nome)
            .all()
        )

    @staticmethod
    def buscar_por_id(id):
        return Usuario.query.get_or_404(id)

    @staticmethod
    def buscar_por_email(email):
        return Usuario.query.filter_by(email=email).first()

    @staticmethod
    def criar(form):
        usuario = Usuario(
            nome=form.nome.data,
            email=form.email.data.lower(),
            is_admin=form.is_admin.data
        )
        usuario.set_senha(form.senha.data)

        db.session.add(usuario)
        db.session.commit()

        return usuario

    @staticmethod
    def atualizar(id, form):
        usuario = Usuario.query.get_or_404(id)

        usuario.nome = form.nome.data
        usuario.email = form.email.data.lower()
        usuario.is_admin = form.is_admin.data

        if form.senha.data:
            usuario.set_senha(form.senha.data)

        db.session.commit()

        return usuario

    @staticmethod
    def excluir(id):
        usuario = Usuario.query.get_or_404(id)
        usuario.ativo = False
        db.session.commit()
