"""add profiles table

Revision ID: 4377ff5f6f23
Revises: 153e40ee69e2
Create Date: 2014-06-06 13:02:21.488400

"""

# revision identifiers, used by Alembic.
revision = '4377ff5f6f23'
down_revision = '153e40ee69e2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'profiles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.Text),
        sa.Column('num_messages_pre', sa.Integer),
        sa.Column('num_messages_post', sa.Integer),
        sa.Column('send_days', sa.Text)
    )


def downgrade():
    op.drop_table('profiles')
