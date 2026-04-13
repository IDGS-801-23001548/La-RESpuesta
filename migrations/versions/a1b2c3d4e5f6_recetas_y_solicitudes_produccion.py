"""recetas y solicitudes de produccion

Revision ID: a1b2c3d4e5f6
Revises: b91a6d0d5bda
Create Date: 2026-04-08 10:15:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = 'b91a6d0d5bda'
branch_labels = None
depends_on = None


def upgrade():
    # ── receta ──
    op.create_table(
        'receta',
        sa.Column('idReceta',     sa.Integer(),     primary_key=True, autoincrement=True),
        sa.Column('nombreReceta', sa.String(100),   nullable=False, unique=True),
        sa.Column('idProducto',   sa.Integer(),     nullable=False),
        sa.Column('idFoto',       sa.String(255),   nullable=True),
        sa.Column('descripcion',  sa.String(500),   nullable=True),
        sa.Column('tipo',         sa.String(20),    nullable=False, server_default='MateriaPrima'),
        sa.ForeignKeyConstraint(['idProducto'], ['producto.idProducto']),
    )

    # ── receta_materia_prima ──
    op.create_table(
        'receta_materia_prima',
        sa.Column('idRecetaMateriaPrima', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('idReceta',             sa.Integer(), nullable=False),
        sa.Column('idMateriaPrima',       sa.Integer(), nullable=False),
        sa.Column('cantidadUsada',        sa.Float(),   nullable=False, server_default='0'),
        sa.ForeignKeyConstraint(['idReceta'],       ['receta.idReceta'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['idMateriaPrima'], ['materia_prima.idMateriaPrima']),
    )

    # ── solicitud_produccion ──
    op.create_table(
        'solicitud_produccion',
        sa.Column('idSolicitud',      sa.Integer(),  primary_key=True, autoincrement=True),
        sa.Column('idReceta',         sa.Integer(),  nullable=False),
        sa.Column('cantidadProducir', sa.Integer(),  nullable=False, server_default='1'),
        sa.Column('fechaSolicitud',   sa.DateTime(), nullable=False),
        sa.Column('fechaCompletada',  sa.DateTime(), nullable=True),
        sa.Column('estatus',          sa.String(20), nullable=False, server_default='Pendiente'),
        sa.Column('idUsuario',        sa.Integer(),  nullable=True),
        sa.Column('notas',            sa.String(500), nullable=True),
        sa.ForeignKeyConstraint(['idReceta'],  ['receta.idReceta']),
        sa.ForeignKeyConstraint(['idUsuario'], ['user.id']),
    )

    # ── solicitud_produccion_detalle ──
    op.create_table(
        'solicitud_produccion_detalle',
        sa.Column('idDetalle',              sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('idSolicitud',            sa.Integer(), nullable=False),
        sa.Column('idMateriaPrima',         sa.Integer(), nullable=False),
        sa.Column('idMateriaPrimaUnitaria', sa.Integer(), nullable=False),
        sa.Column('cantidadConsumida',      sa.Float(),   nullable=False, server_default='0'),
        sa.ForeignKeyConstraint(['idSolicitud'],            ['solicitud_produccion.idSolicitud'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['idMateriaPrima'],         ['materia_prima.idMateriaPrima']),
        sa.ForeignKeyConstraint(['idMateriaPrimaUnitaria'], ['materia_prima_unitaria.idMateriaPrimaUnitaria']),
    )


def downgrade():
    op.drop_table('solicitud_produccion_detalle')
    op.drop_table('solicitud_produccion')
    op.drop_table('receta_materia_prima')
    op.drop_table('receta')
