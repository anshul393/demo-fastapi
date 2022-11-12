"""adding left columns in posts table

Revision ID: 8bafc7c6dcd3
Revises: c0b1950c5037
Create Date: 2022-11-10 22:33:48.688851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8bafc7c6dcd3'
down_revision = 'c0b1950c5037'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable = False,server_default = 'TRUE'))
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable = False,server_default = sa.text('now()')))

    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
