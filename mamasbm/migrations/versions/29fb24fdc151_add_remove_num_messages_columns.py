"""add remove num_messages columns

Revision ID: 29fb24fdc151
Revises: 1c89d076746b
Create Date: 2014-06-30 22:33:15.724342

"""

# revision identifiers, used by Alembic.
revision = '29fb24fdc151'
down_revision = '1c89d076746b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    try:
        op.drop_column('profiles', 'num_messages_post')
        op.drop_column('profiles', 'num_messages_pre')
    except:
        # sqlite bullshit
        pass
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profiles', sa.Column('num_messages_pre', sa.INTEGER(), nullable=True))
    op.add_column('profiles', sa.Column('num_messages_post', sa.INTEGER(), nullable=True))
    ### end Alembic commands ###