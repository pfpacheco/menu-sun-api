"""order_customer

Revision ID: da75318a70bd
Revises: 7ad75d10ec49
Create Date: 2019-10-17 20:58:45.675109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da75318a70bd'
down_revision = '7ad75d10ec49'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_customer', sa.Column('email', sa.String(length=256), nullable=True))
    op.add_column('order_customer', sa.Column('name', sa.String(length=512), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order_customer', 'name')
    op.drop_column('order_customer', 'email')
    # ### end Alembic commands ###