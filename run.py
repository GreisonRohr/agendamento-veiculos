from app import create_app
from app.extensions import db
from app.models import Usuario

app = create_app()

# Setup automático ao iniciar (só no primeiro acesso)
with app.app_context():
    try:
        db.create_all()

        # Cria admin se não existir
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

        # Cria usuário comum se não existir
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

    except Exception as e:
        print(f"Erro no setup: {e}")

if __name__ == "__main__":
    app.run(debug=True)
