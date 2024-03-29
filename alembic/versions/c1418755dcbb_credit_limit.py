"""credit_limit

Revision ID: c1418755dcbb
Revises: de31ffd8a769
Create Date: 2019-10-14 23:42:02.200118

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1418755dcbb'
down_revision = 'de31ffd8a769'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('credit_limit', sa.Float(), nullable=True))
    op.drop_constraint('order_ibfk_2', 'order', type_='foreignkey')
    op.create_foreign_key(None, 'order', 'order_customer', ['customer_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order', type_='foreignkey')
    op.create_foreign_key('order_ibfk_2', 'order', 'customer', ['customer_id'], ['id'])
    op.drop_column('customer', 'credit_limit')
    # ### end Alembic commands ###
