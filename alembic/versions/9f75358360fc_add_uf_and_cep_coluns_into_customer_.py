"""add_uf_and_cep_coluns_into_customer_entity

Revision ID: 9f75358360fc
Revises: 7bbdc8a9d923
Create Date: 2020-05-20 19:36:14.113319

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9f75358360fc'
down_revision = '60145a227b81'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('cep', sa.String(length=9), nullable=True))
    op.add_column('customer', sa.Column('uf', sa.String(length=2), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('customer', 'cep')
    op.drop_column('customer', 'uf')
    # ### end Alembic commands ###
