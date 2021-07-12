"""empty message

Revision ID: 2201116989f9
Revises: 4462ffd5d3ce
Create Date: 2021-07-09 17:32:09.510093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2201116989f9'
down_revision = '4462ffd5d3ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notification', sa.Column('test', sa.String(length=150), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notification', 'test')
    # ### end Alembic commands ###
