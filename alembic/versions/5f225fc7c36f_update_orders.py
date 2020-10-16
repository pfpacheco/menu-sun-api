"""update_orders

Revision ID: 5f225fc7c36f
Revises: 42be5da0f0fb
Create Date: 2019-10-18 12:01:24.849376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f225fc7c36f'
down_revision = '42be5da0f0fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('metafield', sa.Column('order_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'metafield', 'order', ['order_id'], ['id'])
    op.add_column('order', sa.Column('delivery_date', sa.DateTime(), nullable=True))
    op.add_column('order', sa.Column('order_date', sa.DateTime(), nullable=True))
    op.add_column('order_payment', sa.Column('deadline', sa.Integer(), nullable=True))
    op.add_column('order_payment', sa.Column('payment_type', sa.Enum('BOLETO', 'CARTAO_CREDITO', 'DINHEIRO', name='orderpaymenttype'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order_payment', 'payment_type')
    op.drop_column('order_payment', 'deadline')
    op.drop_column('order', 'order_date')
    op.drop_column('order', 'delivery_date')
    op.drop_constraint(None, 'metafield', type_='foreignkey')
    op.drop_column('metafield', 'order_id')
    # ### end Alembic commands ###