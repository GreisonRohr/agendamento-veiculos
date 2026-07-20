from app import create_app
from app.extensions import db
from app.models import Usuario

app = create_app()

with app.app_context():
    print("Criando tabelas...")
    db.create_all()
    print("Tabelas criadas!")

    # Verifica se já existe admin
    admin = Usuario.query.filter_by(email="admin@garagemlab.com").first()
    if admin:
        print("Admin já existe.")
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
        print("✅ Admin criado: admin@garagemlab.com / admin123")

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
        print("✅ Usuário comum criado: usuario@garagemlab.com / usuario123")
    else:
        print("Usuário comum já existe.")
