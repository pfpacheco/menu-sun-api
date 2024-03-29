"""customer

Revision ID: 1c6ea458f448
Revises: 95617ef25f2a
Create Date: 2019-10-17 16:48:25.723555

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c6ea458f448'
down_revision = '95617ef25f2a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('email', sa.String(length=256), nullable=True))
    op.add_column('customer', sa.Column('phone_number', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('customer', 'phone_number')
    op.drop_column('customer', 'email')
    # ### end Alembic commands ###
