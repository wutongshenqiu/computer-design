"""add meeting

Revision ID: 4e5fb07b595c
Revises: 
Create Date: 2021-05-07 19:06:45.276326

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e5fb07b595c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('personal_signature', sa.String(), nullable=True),
    sa.Column('gender', sa.SMALLINT(), nullable=True),
    sa.Column('birth_date', sa.TIMESTAMP(), nullable=True),
    sa.Column('ancestral_home', sa.String(), nullable=True),
    sa.Column('political_status', sa.String(), nullable=True),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('id_card_number', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('face_img_path', sa.String(), nullable=True),
    sa.Column('id_card_path', sa.String(), nullable=True),
    sa.Column('avatar_path', sa.String(), nullable=True),
    sa.Column('is_email_activated', sa.Boolean(), nullable=True),
    sa.Column('is_face_activated', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('avatar_path'),
    sa.UniqueConstraint('face_img_path'),
    sa.UniqueConstraint('id_card_path')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_id_card_number'), 'user', ['id_card_number'], unique=True)
    op.create_index(op.f('ix_user_phone_number'), 'user', ['phone_number'], unique=True)
    op.create_table('address_book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('friend_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['friend_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_address_book_friend_id'), 'address_book', ['friend_id'], unique=False)
    op.create_index(op.f('ix_address_book_id'), 'address_book', ['id'], unique=False)
    op.create_index(op.f('ix_address_book_user_id'), 'address_book', ['user_id'], unique=False)
    op.create_table('meeting',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('meeting_id', sa.Integer(), nullable=False),
    sa.Column('meeting_password', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('meeting_tag', sa.String(), nullable=True),
    sa.Column('type', sa.SMALLINT(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('participants', sa.ARRAY(sa.Integer()), nullable=True),
    sa.Column('designated_participants', sa.ARRAY(sa.Integer()), nullable=True),
    sa.Column('creation_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('end_time', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_meeting_id'), 'meeting', ['id'], unique=False)
    op.create_index(op.f('ix_meeting_meeting_id'), 'meeting', ['meeting_id'], unique=False)
    op.create_index(op.f('ix_meeting_name'), 'meeting', ['name'], unique=False)
    op.create_index(op.f('ix_meeting_owner_id'), 'meeting', ['owner_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_meeting_owner_id'), table_name='meeting')
    op.drop_index(op.f('ix_meeting_name'), table_name='meeting')
    op.drop_index(op.f('ix_meeting_meeting_id'), table_name='meeting')
    op.drop_index(op.f('ix_meeting_id'), table_name='meeting')
    op.drop_table('meeting')
    op.drop_index(op.f('ix_address_book_user_id'), table_name='address_book')
    op.drop_index(op.f('ix_address_book_id'), table_name='address_book')
    op.drop_index(op.f('ix_address_book_friend_id'), table_name='address_book')
    op.drop_table('address_book')
    op.drop_index(op.f('ix_user_phone_number'), table_name='user')
    op.drop_index(op.f('ix_user_id_card_number'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
