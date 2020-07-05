"""add admin login and registration table

Revision ID: daa3b58672ff
Revises: 12a1aea119f3
Create Date: 2020-07-05 16:36:55.909344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'daa3b58672ff'
down_revision = '12a1aea119f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Admins',
    sa.Column('AdminID', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=150), nullable=False),
    sa.Column('Username', sa.String(length=15), nullable=False),
    sa.Column('Email', sa.String(length=120), nullable=False),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('Password', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('AdminID')
    )
    op.create_index(op.f('ix_Admins_Email'), 'Admins', ['Email'], unique=True)
    op.create_index(op.f('ix_Admins_Name'), 'Admins', ['Name'], unique=False)
    op.create_index(op.f('ix_Admins_Username'), 'Admins', ['Username'], unique=True)
    op.add_column('Posts', sa.Column('AdminID', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'Posts', 'Admins', ['AdminID'], ['AdminID'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Posts', type_='foreignkey')
    op.drop_column('Posts', 'AdminID')
    op.drop_index(op.f('ix_Admins_Username'), table_name='Admins')
    op.drop_index(op.f('ix_Admins_Name'), table_name='Admins')
    op.drop_index(op.f('ix_Admins_Email'), table_name='Admins')
    op.drop_table('Admins')
    # ### end Alembic commands ###
