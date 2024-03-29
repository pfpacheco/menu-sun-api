"""column_owner_on_order_status

Revision ID: 52e1c085c21e
Revises: a4543ba2db7a
Create Date: 2020-08-27 09:57:14.928471

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '52e1c085c21e'
down_revision = 'a4543ba2db7a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_status', sa.Column('owner', sa.Enum('MENU', 'SELLER', name='ownertype')))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order_status', 'owner')
    # ### end Alembic commands ###
