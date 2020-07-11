"""add tables

Revision ID: d10e08c81c3b
Revises: 
Create Date: 2020-07-10 08:35:04.148950

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd10e08c81c3b'
down_revision = None
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
    op.create_index(op.f('ix_Contacts_Email'), 'Contacts', ['Email'], unique=False)
    op.create_index(op.f('ix_Contacts_Name'), 'Contacts', ['Name'], unique=False)
    op.create_index(op.f('ix_Contacts_Timestamp'), 'Contacts', ['Timestamp'], unique=False)
    op.create_table('Users',
    sa.Column('UserID', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=150), nullable=False),
    sa.Column('Username', sa.String(length=15), nullable=False),
    sa.Column('Email', sa.String(length=120), nullable=False),
    sa.Column('Bio', sa.String(length=150), nullable=True),
    sa.Column('Password', sa.String(length=128), nullable=False),
    sa.Column('LastSeen', sa.DateTime(), nullable=True),
    sa.Column('LastMessageReadTime', sa.DateTime(), nullable=True),
    sa.Column('RegisteredDate', sa.DateTime(), nullable=False),
    sa.Column('StecAdmin', sa.Boolean(), nullable=False),
    sa.Column('Confirmed', sa.Boolean(), nullable=False),
    sa.Column('ConfirmedDate', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('UserID')
    )
    op.create_index(op.f('ix_Users_Email'), 'Users', ['Email'], unique=True)
    op.create_index(op.f('ix_Users_Name'), 'Users', ['Name'], unique=False)
    op.create_index(op.f('ix_Users_Username'), 'Users', ['Username'], unique=True)
    op.create_table('Notifications',
    sa.Column('N_ID', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=150), nullable=True),
    sa.Column('UserID', sa.Integer(), nullable=True),
    sa.Column('Timestamp', sa.Float(), nullable=True),
    sa.Column('Payload_json', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['UserID'], ['Users.UserID'], ),
    sa.PrimaryKeyConstraint('N_ID')
    )
    op.create_index(op.f('ix_Notifications_Name'), 'Notifications', ['Name'], unique=False)
    op.create_index(op.f('ix_Notifications_Timestamp'), 'Notifications', ['Timestamp'], unique=False)
    op.create_table('Posts',
    sa.Column('PostID', sa.Integer(), nullable=False),
    sa.Column('Subject', sa.String(length=100), nullable=False),
    sa.Column('Body', sa.Text(), nullable=False),
    sa.Column('Timestamp', sa.DateTime(), nullable=True),
    sa.Column('StecAdminID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['StecAdminID'], ['Users.UserID'], ),
    sa.PrimaryKeyConstraint('PostID')
    )
    op.create_index(op.f('ix_Posts_Timestamp'), 'Posts', ['Timestamp'], unique=False)
    op.create_table('UserMessages',
    sa.Column('UserMessageID', sa.Integer(), nullable=False),
    sa.Column('SenderID', sa.Integer(), nullable=True),
    sa.Column('ReceiverID', sa.Integer(), nullable=True),
    sa.Column('Body', sa.String(length=200), nullable=True),
    sa.Column('Timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['ReceiverID'], ['Users.UserID'], ),
    sa.ForeignKeyConstraint(['SenderID'], ['Users.UserID'], ),
    sa.PrimaryKeyConstraint('UserMessageID')
    )
    op.create_index(op.f('ix_UserMessages_Timestamp'), 'UserMessages', ['Timestamp'], unique=False)
    op.create_table('UserPosts',
    sa.Column('UserPostID', sa.Integer(), nullable=False),
    sa.Column('Body', sa.String(length=250), nullable=False),
    sa.Column('Timestamp', sa.DateTime(), nullable=True),
    sa.Column('UserID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['UserID'], ['Users.UserID'], ),
    sa.PrimaryKeyConstraint('UserPostID')
    )
    op.create_index(op.f('ix_UserPosts_Timestamp'), 'UserPosts', ['Timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_UserPosts_Timestamp'), table_name='UserPosts')
    op.drop_table('UserPosts')
    op.drop_index(op.f('ix_UserMessages_Timestamp'), table_name='UserMessages')
    op.drop_table('UserMessages')
    op.drop_index(op.f('ix_Posts_Timestamp'), table_name='Posts')
    op.drop_table('Posts')
    op.drop_index(op.f('ix_Notifications_Timestamp'), table_name='Notifications')
    op.drop_index(op.f('ix_Notifications_Name'), table_name='Notifications')
    op.drop_table('Notifications')
    op.drop_index(op.f('ix_Users_Username'), table_name='Users')
    op.drop_index(op.f('ix_Users_Name'), table_name='Users')
    op.drop_index(op.f('ix_Users_Email'), table_name='Users')
    op.drop_table('Users')
    op.drop_index(op.f('ix_Contacts_Timestamp'), table_name='Contacts')
    op.drop_index(op.f('ix_Contacts_Name'), table_name='Contacts')
    op.drop_index(op.f('ix_Contacts_Email'), table_name='Contacts')
    op.drop_table('Contacts')
    # ### end Alembic commands ###
