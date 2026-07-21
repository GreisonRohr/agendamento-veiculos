"""add usuario_id to agendamentos

Revision ID: add_usuario_id
Revises: 
Create Date: 2026-07-20 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_usuario_id'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Adiciona coluna usuario_id se não existir
    op.add_column('agendamentos', sa.Column('usuario_id', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('agendamentos', 'usuario_id')
