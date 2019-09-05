"""articles table

Revision ID: ac81a5dc3b46
Revises: d5a91ed37187
Create Date: 2019-03-23 16:32:27.335989

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac81a5dc3b46'
down_revision = 'd5a91ed37187'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('article',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=True),
    sa.Column('tag', sa.String(length=80), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('pic_path', sa.String(length=320), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_article_tag'), 'article', ['tag'], unique=False)
    op.create_index(op.f('ix_article_title'), 'article', ['title'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_article_title'), table_name='article')
    op.drop_index(op.f('ix_article_tag'), table_name='article')
    op.drop_table('article')
    # ### end Alembic commands ###
