"""Update supplier unique constraint

Revision ID: a02b1987d645
Revises: 78453a88a38e
Create Date: 2026-07-03 04:59:34.647896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a02b1987d645'
down_revision = '78453a88a38e'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if 'suppliers' not in inspector.get_table_names():
        return

    existing_constraints = [
        c['name'] for c in inspector.get_unique_constraints('suppliers')
    ]

    if 'uq_business_supplier_name' in existing_constraints:
        # Already applied (e.g. db.create_all() created it from the model).
        return

    with op.batch_alter_table('suppliers', schema=None) as batch_op:
        # Only drop the old constraint if it actually exists.
        if 'suppliers_supplier_name_key' in existing_constraints:
            batch_op.drop_constraint('suppliers_supplier_name_key', type_='unique')
        batch_op.create_unique_constraint(
            'uq_business_supplier_name', ['business_id', 'supplier_name'],
        )


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if 'suppliers' not in inspector.get_table_names():
        return

    existing_constraints = [
        c['name'] for c in inspector.get_unique_constraints('suppliers')
    ]

    with op.batch_alter_table('suppliers', schema=None) as batch_op:
        if 'uq_business_supplier_name' in existing_constraints:
            batch_op.drop_constraint('uq_business_supplier_name', type_='unique')
        if 'suppliers_supplier_name_key' not in existing_constraints:
            batch_op.create_unique_constraint(
                'suppliers_supplier_name_key', ['supplier_name'],
            )
