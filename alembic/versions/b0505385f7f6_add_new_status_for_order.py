"""add_new_status_for_order

Revision ID: 60145a227b81
Revises: a27b6e57783e
Create Date: 2020-06-04 12:13:36.846121

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '60145a227b81'
down_revision = 'a27b6e57783e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('order_status', 'status',
                    existing_type=mysql.ENUM('NEW', 'APPROVED', 'INVOICED', 'SHIPPED', 'DELIVERED',
                                             'CANCELED', 'SHIPMENT_EXCEPTION', 'PAYMENT_OVERDUE'),
                    type_=sa.Enum('NEW', 'APPROVED', 'INVOICED', 'SHIPPED', 'DELIVERED',
                                  'SHIPMENT_EXCEPTION', 'PAYMENT_OVERDUE',
                                  'NEW_ORDER',
                                  'SELLER_REVIEW',
                                  'PROCESSING',
                                  'ORDER_INVOICED',
                                  'PENDING',
                                  'CANCELED',
                                  'CREDIT_MENU',
                                  'CLOSED', name='status'),
                    existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('order_status', 'status',
                    existing_type=sa.Enum('NEW', 'APPROVED', 'INVOICED', 'SHIPPED', 'DELIVERED',
                                          'SHIPMENT_EXCEPTION', 'PAYMENT_OVERDUE',
                                          'NEW_ORDER',
                                          'SELLER_REVIEW',
                                          'PROCESSING',
                                          'ORDER_INVOICED',
                                          'PENDING',
                                          'CANCELED',
                                          'DELIVERED',
                                          'CREDIT_MENU',
                                          'CLOSED', name='status'),
                    type_=mysql.ENUM('NEW', 'APPROVED', 'INVOICED', 'SHIPPED', 'DELIVERED',
                                     'CANCELED', 'SHIPMENT_EXCEPTION', 'PAYMENT_OVERDUE'),
                    existing_nullable=False)
    # ### end Alembic commands ###
