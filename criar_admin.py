from app import create_app
from app.extensions import db
from app.models import Usuario

app = create_app()

with app.app_context():
    # Verifica se já existe admin
    admin = Usuario.query.filter_by(email="admin@garagemlab.com").first()
    if admin:
        print("=" * 50)
        print("Admin já existe!")
        print(f"E-mail: {admin.email}")
        print("Senha: admin123")
        print("=" * 50)
    else:
        admin = Usuario(
            nome="Administrador",
            email="admin@garagemlab.com",
            is_admin=True,
            ativo=True
        )
        admin.set_senha("admin123")
        db.session.add(admin)
        db.session.commit()
        print("=" * 50)
        print("✅ Admin criado com sucesso!")
        print("E-mail: admin@garagemlab.com")
        print("Senha: admin123")
        print("=" * 50)

    # Cria um usuário comum de exemplo
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
        print("✅ Usuário comum criado!")
        print("E-mail: usuario@garagemlab.com")
        print("Senha: usuario123")
        print("=" * 50)
    else:
        print("Usuário comum já existe!")
        print(f"E-mail: {usuario.email}")
        print("Senha: usuario123")
        print("=" * 50)
