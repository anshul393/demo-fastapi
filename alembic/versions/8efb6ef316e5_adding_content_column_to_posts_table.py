"""adding content column to posts table

Revision ID: 8efb6ef316e5
Revises: 38e6a00da91e
Create Date: 2022-11-10 21:48:29.622414

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8efb6ef316e5'
down_revision = '38e6a00da91e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable = False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
