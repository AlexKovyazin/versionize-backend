"""users validated field default

Revision ID: efaeed69e063
Revises: 46a9f083b561
Create Date: 2025-10-14 17:16:24.094113

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'efaeed69e063'
down_revision: Union[str, Sequence[str], None] = '46a9f083b561'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('users', 'validated', existing_type=sa.Boolean, server_default=text('false'))


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('users', 'validated', existing_type=sa.Boolean, server_default=None)
