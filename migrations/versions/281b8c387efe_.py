"""empty message

Revision ID: 281b8c387efe
Revises: 162a268c643e
Create Date: 2023-01-05 22:47:39.494847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '281b8c387efe'
down_revision = '162a268c643e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=128), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###
