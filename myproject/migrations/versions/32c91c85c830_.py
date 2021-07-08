"""empty message

Revision ID: 32c91c85c830
Revises: c40edcc364a3
Create Date: 2021-07-06 21:20:21.799846

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32c91c85c830'
down_revision = 'c40edcc364a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###