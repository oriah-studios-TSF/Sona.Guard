
"""Add units and resident unit assignment

Revision ID: c8159f6bd435
Revises: e12d2d0ea928
"""

from alembic import op
import sqlalchemy as sa


revision = 'c8159f6bd435'
down_revision = 'e12d2d0ea928'
branch_labels = None
depends_on = None


def upgrade():
    # Create the units table.
    op.create_table(
        'units',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('property_id', sa.Integer(), nullable=False),
        sa.Column('unit_number', sa.String(length=50), nullable=False),
        sa.Column('unit_type', sa.String(length=30), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ['property_id'],
            ['properties.id']
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint(
            'property_id',
            'unit_number',
            name='uq_units_property_unit_number'
        )
    )

    # Add the unit reference to existing residents.
    with op.batch_alter_table('residents') as batch_op:
        batch_op.add_column(
            sa.Column('unit_id', sa.Integer(), nullable=True)
        )
        batch_op.create_foreign_key(
            'fk_residents_unit_id_units',
            'units',
            ['unit_id'],
            ['id']
        )

    # Create one unit for each distinct estate/unit combination.
    # Existing residents keep their original unit_number values.
    op.execute(sa.text("""
        INSERT INTO units (
            property_id,
            unit_number,
            unit_type,
            is_active,
            created_at,
            updated_at
        )
        SELECT DISTINCT
            property_id,
            unit_number,
            'house',
            1,
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP
        FROM residents
        WHERE unit_number IS NOT NULL
          AND TRIM(unit_number) != ''
    """))

    # Connect each existing resident to the matching unit.
    op.execute(sa.text("""
        UPDATE residents
        SET unit_id = (
            SELECT units.id
            FROM units
            WHERE units.property_id = residents.property_id
              AND units.unit_number = residents.unit_number
        )
        WHERE EXISTS (
            SELECT 1
            FROM units
            WHERE units.property_id = residents.property_id
              AND units.unit_number = residents.unit_number
        )
    """))


def downgrade():
    # Remove the resident-to-unit relationship first.
    with op.batch_alter_table('residents') as batch_op:
        batch_op.drop_constraint(
            'fk_residents_unit_id_units',
            type_='foreignkey'
        )
        batch_op.drop_column('unit_id')

    # Remove the units table.
    op.drop_table('units')
