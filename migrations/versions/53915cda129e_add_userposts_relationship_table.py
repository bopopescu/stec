"""add userposts relationship table

Revision ID: 53915cda129e
Revises: 99247dd9525e
Create Date: 2020-07-03 22:12:57.013003

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '53915cda129e'
down_revision = '99247dd9525e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('posts_ibfk_1', 'Posts', type_='foreignkey')
    op.drop_column('Posts', 'UserID')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Posts', sa.Column('UserID', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('posts_ibfk_1', 'Posts', 'Users', ['UserID'], ['UserID'])
    # ### end Alembic commands ###
