"""database v2

Revision ID: f5a670b79dc1
Revises: e1165516799a
Create Date: 2018-01-15 00:18:38.315521

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5a670b79dc1'
down_revision = 'e1165516799a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('company', sa.Column('Slogan', sa.String(length=256), nullable=True))
    op.add_column('company', sa.Column('address', sa.String(length=256), nullable=True))
    op.add_column('company', sa.Column('description', sa.String(length=1024), nullable=True))
    op.add_column('company', sa.Column('logo_url', sa.String(length=256), nullable=True))
    op.add_column('company', sa.Column('website', sa.String(length=256), nullable=True))
    op.add_column('job', sa.Column('address', sa.String(length=256), nullable=True))
    op.add_column('job', sa.Column('company_id', sa.Integer(), nullable=True))
    op.add_column('job', sa.Column('degree_request', sa.String(length=32), nullable=True))
    op.add_column('job', sa.Column('description', sa.String(length=1024), nullable=True))
    op.add_column('job', sa.Column('exp_request', sa.String(length=32), nullable=True))
    op.add_column('job', sa.Column('job_request', sa.String(length=1024), nullable=True))
    op.add_column('job', sa.Column('salary_range', sa.String(length=128), nullable=True))
    op.create_foreign_key(None, 'job', 'company', ['company_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'job', type_='foreignkey')
    op.drop_column('job', 'salary_range')
    op.drop_column('job', 'job_request')
    op.drop_column('job', 'exp_request')
    op.drop_column('job', 'description')
    op.drop_column('job', 'degree_request')
    op.drop_column('job', 'company_id')
    op.drop_column('job', 'address')
    op.drop_column('company', 'website')
    op.drop_column('company', 'logo_url')
    op.drop_column('company', 'description')
    op.drop_column('company', 'address')
    op.drop_column('company', 'Slogan')
    # ### end Alembic commands ###
