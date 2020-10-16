"""constraint

Revision ID: 95617ef25f2a
Revises: 51f0db479e4f
Create Date: 2019-10-17 15:04:11.834349

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95617ef25f2a'
down_revision = '51f0db479e4f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('integration_date', sa.DateTime(), nullable=True))
    op.create_unique_constraint('_seller_id_order_id', 'order', ['seller_id', 'order_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('_seller_id_order_id', 'order', type_='unique')
    op.drop_column('order', 'integration_date')
    # ### end Alembic commands ###