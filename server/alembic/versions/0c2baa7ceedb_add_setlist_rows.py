"""Add setlist rows

Revision ID: 0c2baa7ceedb
Revises: cf609a4794ac
Create Date: 2022-07-09 19:34:39.263718

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c2baa7ceedb'
down_revision = 'cf609a4794ac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('setlists', sa.Column('name', sa.String(), nullable=True))
    op.add_column('setlists', sa.Column('comments', sa.String(), nullable=True))
    op.add_column('setlists', sa.Column('created', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
    op.add_column('setlists', sa.Column('tags', sa.String(), nullable=True))
    op.add_column('setlists', sa.Column('setup', sa.String(), nullable=True))
    op.add_column('setlists', sa.Column('last_played', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
    op.add_column('setlists', sa.Column('setlist', sa.JSON(), nullable=True))
    op.drop_column('setlists', 'title')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('setlists', sa.Column('title', sa.VARCHAR(), nullable=True))
    op.drop_column('setlists', 'setlist')
    op.drop_column('setlists', 'last_played')
    op.drop_column('setlists', 'setup')
    op.drop_column('setlists', 'tags')
    op.drop_column('setlists', 'created')
    op.drop_column('setlists', 'comments')
    op.drop_column('setlists', 'name')
    # ### end Alembic commands ###