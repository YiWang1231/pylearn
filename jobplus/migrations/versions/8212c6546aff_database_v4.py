"""database V4

Revision ID: 8212c6546aff
Revises: f5a670b79dc1
Create Date: 2018-01-17 14:19:12.725192

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8212c6546aff'
down_revision = 'f5a670b79dc1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('description', sa.String(length=1024), nullable=True))
    op.add_column('user', sa.Column('education', sa.String(length=24), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'education')
    op.drop_column('user', 'description')
    # ### end Alembic commands ###
