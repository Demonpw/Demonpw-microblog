"""Articles table

Revision ID: 3564f55c0d1d
Revises: 5b66fcacd849
Create Date: 2019-03-23 22:37:39.642664

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3564f55c0d1d'
down_revision = '5b66fcacd849'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'body')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('body', mysql.TEXT(), nullable=True))
    # ### end Alembic commands ###
