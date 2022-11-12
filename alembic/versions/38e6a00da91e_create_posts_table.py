"""create posts table

Revision ID: 38e6a00da91e
Revises: 
Create Date: 2022-11-10 21:35:47.288467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38e6a00da91e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable = False,primary_key = True),sa.Column('title',sa.String(),nullable = False))

    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
