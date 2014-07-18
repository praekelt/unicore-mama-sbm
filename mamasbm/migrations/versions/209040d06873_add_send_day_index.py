"""add send_day index

Revision ID: 209040d06873
Revises: 1c9e829abd8e
Create Date: 2014-07-16 16:13:09.723638

"""

# revision identifiers, used by Alembic.
revision = '209040d06873'
down_revision = '1c9e829abd8e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index('message_profile_send_day_index', 'message_profiles', ['send_day'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('message_profile_send_day_index', table_name='message_profiles')
    ### end Alembic commands ###