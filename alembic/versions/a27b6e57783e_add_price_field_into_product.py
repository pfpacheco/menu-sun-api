"""add_price_field_into_product

Revision ID: a27b6e57783e
Revises: 7bbdc8a9d923
Create Date: 2020-05-15 16:10:48.441492

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a27b6e57783e'
down_revision = '7bbdc8a9d923'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('customer', 'active',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=False)
    op.add_column('product', sa.Column('list_price', sa.Float(), nullable=True))
    op.add_column('product', sa.Column('sale_price', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'sale_price')
    op.drop_column('product', 'list_price')
    op.alter_column('customer', 'active',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False)
    # ### end Alembic commands ###
