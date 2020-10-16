"""payment_terms

Revision ID: 53ed3c2c2e14
Revises: 23e1a34f934c
Create Date: 2019-10-09 22:25:38.451405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53ed3c2c2e14'
down_revision = '23e1a34f934c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payment_terms',
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('updated_date', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('deadline', sa.Integer(), nullable=True),
    sa.Column('payment_type', sa.Enum('BOLETO', 'CARTAO_CREDITO', 'DINHEIRO', name='paymenttype'), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payment_terms')
    # ### end Alembic commands ###