"""update contact table

Revision ID: d992985cb912
Revises: 83a30646da6f
Create Date: 2020-07-10 16:54:37.669337

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd992985cb912'
down_revision = '83a30646da6f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Contacts', 'LastEnquiryReadTime')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Contacts', sa.Column('LastEnquiryReadTime', mysql.DATETIME(), nullable=True))
    # ### end Alembic commands ###
