"""add few columns to posts table

Revision ID: bf31d4205c0d
Revises: 92114b4f3f65
Create Date: 2022-03-16 16:56:23.614428

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf31d4205c0d'
down_revision = '92114b4f3f65'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"))
    pass


def downgrade():
    op.drop_column("posts", "content")
    op.drop_column("posts", "published")
    pass
