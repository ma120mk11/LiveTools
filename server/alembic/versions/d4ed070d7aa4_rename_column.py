"""Rename column

Revision ID: d4ed070d7aa4
Revises: 0c2baa7ceedb
Create Date: 2022-07-10 10:48:51.858679

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = 'd4ed070d7aa4'
down_revision = '0c2baa7ceedb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('setlists', schema=None) as batch_op: batch_op.alter_column('setlist', new_column_name='actions')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('setlists', schema=None) as batch_op: batch_op.alter_column('actions', new_column_name='setlist')
    # ### end Alembic commands ###
