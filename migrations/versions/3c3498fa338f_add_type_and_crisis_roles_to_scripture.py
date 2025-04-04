"""Add type and crisis_roles to Scripture

Revision ID: 3c3498fa338f
Revises: 0d5590a3138b
Create Date: 2025-03-24 15:07:43.285576

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '3c3498fa338f'
down_revision = '0d5590a3138b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('scriptures', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('crisis_roles', sqlite.JSON(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('scriptures', schema=None) as batch_op:
        batch_op.drop_column('crisis_roles')
        batch_op.drop_column('type')

    # ### end Alembic commands ###
