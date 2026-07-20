#!/bin/bash
echo "=========================================="
echo "PRE-DEPLOY: Configurando banco de dados"
echo "=========================================="

python -c "
import os
print('DATABASE_URL:', os.getenv('DATABASE_URL', 'NAO CONFIGURADO')[:50])

from app import create_app
from app.extensions import db
from app.models import Usuario

app = create_app()
with app.app_context():
    print('Criando tabelas...')
    db.create_all()
    print('Tabelas criadas!')

    # Cria admin
    admin = Usuario.query.filter_by(email='admin@garagemlab.com').first()
    if not admin:
        print('Criando admin...')
        admin = Usuario(nome='Administrador', email='admin@garagemlab.com', is_admin=True, ativo=True)
        admin.set_senha('admin123')
        db.session.add(admin)
        db.session.commit()
        print('Admin criado!')
    else:
        print('Admin ja existe')

    # Cria usuario comum
    usuario = Usuario.query.filter_by(email='usuario@garagemlab.com').first()
    if not usuario:
        print('Criando usuario comum...')
        usuario = Usuario(nome='Usuario Comum', email='usuario@garagemlab.com', is_admin=False, ativo=True)
        usuario.set_senha('usuario123')
        db.session.add(usuario)
        db.session.commit()
        print('Usuario comum criado!')
    else:
        print('Usuario comum ja existe')

    print('Usuarios no banco:', Usuario.query.count())
"

echo "=========================================="
echo "PRE-DEPLOY CONCLUIDO"
echo "=========================================="
