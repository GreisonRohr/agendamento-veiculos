from app import create_app
from app.extensions import db
from app.models import Usuario

app = create_app()

# Setup automático ao iniciar
with app.app_context():
    try:
        # Cria tabelas que não existem
        db.create_all()

        # Tenta adicionar usuario_id se não existir (PostgreSQL)
        from sqlalchemy import inspect, text
        inspector = inspect(db.engine)
        colunas = [c['name'] for c in inspector.get_columns('agendamentos')]

        if 'usuario_id' not in colunas:
            print("Adicionando coluna usuario_id...")
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE agendamentos ADD COLUMN usuario_id INTEGER"))
                conn.commit()
            print("Coluna usuario_id adicionada!")

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
            print("Admin criado")

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
            print("Usuario comum criado")

    except Exception as e:
        print(f"Erro no setup: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    app.run(debug=True)
