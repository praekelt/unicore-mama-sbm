"""create default table

Revision ID: 153e40ee69e2
Revises: None
Create Date: 2014-05-29 17:10:20.979125

"""

# revision identifiers, used by Alembic.
revision = '153e40ee69e2'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'models',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Text),
        sa.Column('value', sa.Integer)
    )


def downgrade():
    op.drop_table('models')
