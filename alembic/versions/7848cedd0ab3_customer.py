"""customer

Revision ID: 7848cedd0ab3
Revises: f43523fb0177
Create Date: 2019-10-22 15:32:22.660625

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7848cedd0ab3'
down_revision = 'f43523fb0177'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('order_ibfk_5', 'order', type_='foreignkey')
    op.drop_table('order_customer')
    op.create_foreign_key(None, 'order', 'customer', ['customer_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order', type_='foreignkey')
    op.create_foreign_key('order_ibfk_5', 'order', 'order_customer', ['customer_id'], ['id'])
    op.create_table('order_customer',
    sa.Column('created_date', mysql.DATETIME(), nullable=False),
    sa.Column('updated_date', mysql.DATETIME(), nullable=True),
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('document', mysql.VARCHAR(length=16), nullable=False),
    sa.Column('email', mysql.VARCHAR(length=256), nullable=True),
    sa.Column('name', mysql.VARCHAR(length=512), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
