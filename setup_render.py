import os
import sys

print("=" * 60)
print("SETUP RENDER - INICIANDO")
print("=" * 60)

try:
    from app import create_app
    from app.extensions import db
    from app.models import Usuario

    app = create_app()

    with app.app_context():
        # Verifica qual banco está sendo usado
        database_url = os.getenv("DATABASE_URL", "NÃO CONFIGURADO")
        if database_url != "NÃO CONFIGURADO":
            print(f"DATABASE_URL: {database_url[:60]}...")
        else:
            print(f"DATABASE_URL: {database_url}")

        print("\nCriando tabelas...")
        db.create_all()
        print("✅ Tabelas criadas!")

        # Lista tabelas
        try:
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tabelas = inspector.get_table_names()
            print(f"Tabelas no banco: {tabelas}")
        except Exception as e:
            print(f"Não foi possível listar tabelas: {e}")

        # Verifica/cria admin
        print("\nVerificando usuário admin...")
        admin = Usuario.query.filter_by(email="admin@garagemlab.com").first()

        if admin:
            print(f"✅ Admin já existe: {admin.email}")
        else:
            print("Criando admin...")
            admin = Usuario(
                nome="Administrador",
                email="admin@garagemlab.com",
                is_admin=True,
                ativo=True
            )
            admin.set_senha("admin123")
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin criado!")

        # Verifica/cria usuário comum
        print("\nVerificando usuário comum...")
        usuario = Usuario.query.filter_by(email="usuario@garagemlab.com").first()

        if usuario:
            print(f"✅ Usuário comum já existe: {usuario.email}")
        else:
            print("Criando usuário comum...")
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

        # Lista todos
        print("\n" + "=" * 60)
        print("USUÁRIOS NO BANCO:")
        todos = Usuario.query.all()
        for u in todos:
            print(f"  - {u.email} | Admin: {u.is_admin}")
        print("=" * 60)

except Exception as e:
    print(f"❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    # Não sai com erro para não impedir o gunicorn de iniciar
    print("\nContinuando mesmo com erro...")

print("\n✅ SETUP CONCLUÍDO")
print("=" * 60)
