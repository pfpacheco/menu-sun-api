"""add_serbom_integration_type

Revision ID: 2fc4c18f1104
Revises: a27b6e57783e
Create Date: 2020-06-16 14:50:12.246513

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2fc4c18f1104'
down_revision = '768263ad33ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('seller', 'integration_type',
                    existing_type=mysql.ENUM('NOT_IMPLEMENTED', 'PROMAX', 'PERNOD', 'BRF'),
                    type_=sa.Enum('NOT_IMPLEMENTED', 'PROMAX', 'PERNOD', 'BRF', 'ARYZTA', 'BENJAMIN',
                                  name='integrationtype'),
                    existing_nullable=False,
                    existing_server_default=sa.text("'NOT_IMPLEMENTED'"))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('seller', 'integration_type',
                    existing_type=sa.Enum('NOT_IMPLEMENTED', 'PROMAX', 'PERNOD', 'BRF', 'ARYZTA', 'BENJAMIN',
                                          name='integrationtype'),
                    type_=mysql.ENUM('NOT_IMPLEMENTED', 'PROMAX', 'PERNOD', 'BRF'),
                    existing_nullable=False,
                    existing_server_default=sa.text("'NOT_IMPLEMENTED'"))
    # ### end Alembic commands ###
