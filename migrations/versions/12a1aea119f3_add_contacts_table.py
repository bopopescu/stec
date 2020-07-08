"""add contacts table

Revision ID: 12a1aea119f3
Revises: 53915cda129e
Create Date: 2020-07-05 00:40:32.000425

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12a1aea119f3'
down_revision = '53915cda129e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Contacts',
    sa.Column('ContactID', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=150), nullable=False),
    sa.Column('Email', sa.String(length=120), nullable=False),
    sa.Column('Enquiry', sa.Text(), nullable=False),
    sa.Column('Timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('ContactID')
    )
    op.create_index(op.f('ix_Contacts_Email'), 'Contacts', ['Email'], unique=True)
    op.create_index(op.f('ix_Contacts_Name'), 'Contacts', ['Name'], unique=False)
    op.create_index(op.f('ix_Contacts_Timestamp'), 'Contacts', ['Timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Contacts_Timestamp'), table_name='Contacts')
    op.drop_index(op.f('ix_Contacts_Name'), table_name='Contacts')
    op.drop_index(op.f('ix_Contacts_Email'), table_name='Contacts')
    op.drop_table('Contacts')
    # ### end Alembic commands ###