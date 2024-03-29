"""adding_promo_price

Revision ID: 429e298c85f2
Revises: 0f8e8c8f654f
Create Date: 2020-06-23 15:16:33.612984

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '429e298c85f2'
down_revision = '0f8e8c8f654f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('product', sa.Column('promo_price', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'promo_price')
    # ### end Alembic commands ###

