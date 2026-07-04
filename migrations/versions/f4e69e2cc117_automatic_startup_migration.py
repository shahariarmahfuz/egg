"""Automatic startup migration

Revision ID: f4e69e2cc117
Revises: 8e8dadea4edd
Create Date: 2026-07-03 11:33:20.062983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4e69e2cc117'
down_revision = 'a02b1987d645'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if 'admin' not in inspector.get_table_names():
        return

    existing_columns = [c['name'] for c in inspector.get_columns('admin')]
    if 'avatar_seed' in existing_columns:
        return

    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatar_seed', sa.String(length=50), nullable=True))


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if 'admin' not in inspector.get_table_names():
        return

    existing_columns = [c['name'] for c in inspector.get_columns('admin')]
    if 'avatar_seed' not in existing_columns:
        return

    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.drop_column('avatar_seed')
