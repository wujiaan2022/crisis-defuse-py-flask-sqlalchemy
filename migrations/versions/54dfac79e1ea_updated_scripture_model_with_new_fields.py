"""Updated Scripture model with new fields

Revision ID: 54dfac79e1ea
Revises: 
Create Date: 2025-03-09 19:24:54.341345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54dfac79e1ea'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('scriptures', schema=None) as batch_op:
        batch_op.add_column(sa.Column('summary', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('introduction', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('precautions', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('daily_recitation', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('prayer_statement', sa.Text(), nullable=True))
        batch_op.drop_column('info')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('scriptures', schema=None) as batch_op:
        batch_op.add_column(sa.Column('info', sa.TEXT(), nullable=True))
        batch_op.drop_column('prayer_statement')
        batch_op.drop_column('daily_recitation')
        batch_op.drop_column('precautions')
        batch_op.drop_column('introduction')
        batch_op.drop_column('summary')

    # ### end Alembic commands ###
