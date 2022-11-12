"""Add user table

Revision ID: 972bbe185b33
Revises: 8efb6ef316e5
Create Date: 2022-11-10 21:53:42.798833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '972bbe185b33'
down_revision = '8efb6ef316e5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                            sa.Column('id',sa.Integer(),nullable = False),
                            sa.Column('email',sa.String(),nullable = False),
                            sa.Column('password',sa.String(),nullable = False),
                            sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable = False),
                            sa.PrimaryKeyConstraint('id'),
                            sa.UniqueConstraint('email')
                            )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
