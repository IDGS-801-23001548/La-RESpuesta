"""Trazabilidad en orden_compra y fechaCaducidad en canal

Revision ID: d3f8a1b2c4e5
Revises: ca8efd558bfa
Create Date: 2026-04-12 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd3f8a1b2c4e5'
down_revision = 'ca8efd558bfa'
branch_labels = None
depends_on = None


def upgrade():
    # Trazabilidad: quien creo la orden de compra
    op.add_column('orden_compra', sa.Column('idUsuario', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_orden_compra_usuario', 'orden_compra', 'user', ['idUsuario'], ['id'])

    # Trazabilidad: quien pago al proveedor
    op.add_column('orden_compra', sa.Column('idUsuarioPago', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_orden_compra_usuario_pago', 'orden_compra', 'user', ['idUsuarioPago'], ['id'])

    # Fecha de caducidad en canal (auto-calculada al recibir la orden)
    op.add_column('canal', sa.Column('fechaCaducidad', sa.Date(), nullable=True))


def downgrade():
    op.drop_column('canal', 'fechaCaducidad')
    op.drop_constraint('fk_orden_compra_usuario_pago', 'orden_compra', type_='foreignkey')
    op.drop_column('orden_compra', 'idUsuarioPago')
    op.drop_constraint('fk_orden_compra_usuario', 'orden_compra', type_='foreignkey')
    op.drop_column('orden_compra', 'idUsuario')
