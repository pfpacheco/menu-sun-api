"""seller_metafield

Revision ID: 903f578cf8de
Revises: 28d6dc996c76
Create Date: 2019-10-21 23:35:16.010217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '903f578cf8de'
down_revision = '28d6dc996c76'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('seller_metafield',
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('updated_date', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(length=64), nullable=True),
    sa.Column('value', sa.String(length=64), nullable=True),
    sa.Column('seller_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['seller_id'], ['seller.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('seller_metafield')
    # ### end Alembic commands ###