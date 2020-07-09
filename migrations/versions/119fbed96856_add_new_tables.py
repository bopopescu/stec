"""add new tables

Revision ID: 119fbed96856
Revises: b6616bc04183
Create Date: 2020-07-09 07:54:44.275728

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '119fbed96856'
down_revision = 'b6616bc04183'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('UserMessages',
    sa.Column('UserMessageID', sa.Integer(), nullable=False),
    sa.Column('SenderID', sa.Integer(), nullable=True),
    sa.Column('ReceiverID', sa.Integer(), nullable=True),
    sa.Column('Body', sa.String(length=140), nullable=True),
    sa.Column('Timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['ReceiverID'], ['Users.UserID'], ),
    sa.ForeignKeyConstraint(['SenderID'], ['Users.UserID'], ),
    sa.PrimaryKeyConstraint('UserMessageID')
    )
    op.create_index(op.f('ix_UserMessages_Timestamp'), 'UserMessages', ['Timestamp'], unique=False)
    op.add_column('Admins', sa.Column('LastSeen', sa.DateTime(), nullable=True))
    op.drop_column('Admins', 'LastSeen')
    op.add_column('Users', sa.Column('LastMessageReadTime', sa.DateTime(), nullable=True))
    op.add_column('Users', sa.Column('LastSeen', sa.DateTime(), nullable=True))
    op.drop_column('Users', 'Gender')
    op.drop_column('Users', 'LastSeen')
    op.drop_column('Users', 'DateOfBirthday')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Users', sa.Column('DateOfBirthday', mysql.DATETIME(), nullable=True))
    op.add_column('Users', sa.Column('LastSeen', mysql.DATETIME(), nullable=True))
    op.add_column('Users', sa.Column('Gender', mysql.VARCHAR(length=30), nullable=True))
    op.drop_column('Users', 'LastSeen')
    op.drop_column('Users', 'LastMessageReadTime')
    op.add_column('Admins', sa.Column('LastSeen', mysql.DATETIME(), nullable=True))
    op.drop_column('Admins', 'LastSeen')
    op.drop_index(op.f('ix_UserMessages_Timestamp'), table_name='UserMessages')
    op.drop_table('UserMessages')
    # ### end Alembic commands ###
