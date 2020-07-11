"""update a column in contacts

Revision ID: 83a30646da6f
Revises: d10e08c81c3b
Create Date: 2020-07-10 15:49:38.447964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83a30646da6f'
down_revision = 'd10e08c81c3b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Contacts', sa.Column('LastEnquiryReadTime', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Contacts', 'LastEnquiryReadTime')
    # ### end Alembic commands ###
