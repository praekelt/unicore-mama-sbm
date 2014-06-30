"""add message models

Revision ID: 18b7e31bc9ed
Revises: 40e18b7ea943
Create Date: 2014-06-30 14:45:08.429232

"""

# revision identifiers, used by Alembic.
revision = '18b7e31bc9ed'
down_revision = '40e18b7ea943'

from alembic import op
import sqlalchemy as sa
from mamasbm.models import UUID


def upgrade():
    # commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'messages',
        sa.Column('uuid', UUID(), nullable=False),
        sa.Column('week', sa.Integer(), nullable=True),
        sa.Column('text', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table(
        'message_profiles',
        sa.Column('uuid', UUID(), nullable=False),
        sa.Column('name', sa.Text(), nullable=True),
        sa.Column('profile_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['profile_id'], ['profiles.uuid'], ),
        sa.PrimaryKeyConstraint('uuid')
    )
    # end Alembic commands ###


def downgrade():
    # commands auto generated by Alembic - please adjust! ###
    op.drop_table('message_profiles')
    op.drop_table('messages')
    # end Alembic commands ###
