"""remove_metafield

Revision ID: 05eff8379912
Revises: 0d17252244a3
Create Date: 2019-10-18 15:09:49.973627

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '05eff8379912'
down_revision = '0d17252244a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order_metafield',
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('updated_date', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(length=64), nullable=True),
    sa.Column('value', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('metafield')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('metafield',
    sa.Column('created_date', mysql.DATETIME(), nullable=False),
    sa.Column('updated_date', mysql.DATETIME(), nullable=True),
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('customer_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('key', mysql.VARCHAR(length=64), nullable=True),
    sa.Column('value', mysql.VARCHAR(length=64), nullable=True),
    sa.Column('product_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('order_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], name='metafield_ibfk_1'),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], name='metafield_ibfk_3'),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], name='metafield_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.drop_table('order_metafield')
    # ### end Alembic commands ###
