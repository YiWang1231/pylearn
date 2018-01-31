"""V12

Revision ID: 7d45cea9943b
Revises: 3b8c054d2114
Create Date: 2018-01-23 13:04:39.317940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d45cea9943b'
down_revision = '3b8c054d2114'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('delivery', sa.Column('job_address', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('delivery', 'job_address')
    # ### end Alembic commands ###