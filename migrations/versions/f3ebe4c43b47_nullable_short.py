"""nullable short

Revision ID: f3ebe4c43b47
Revises: bec3e18d8989
Create Date: 2023-06-17 13:53:33.350277

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3ebe4c43b47'
down_revision = 'bec3e18d8989'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('url_map', 'short',
               existing_type=sa.VARCHAR(length=16),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('url_map', 'short',
               existing_type=sa.VARCHAR(length=16),
               nullable=True)
    # ### end Alembic commands ###
