"""simple

Revision ID: 437bb15cc3f4
Revises: bdd1c2253762
Create Date: 2018-01-05 15:03:26.662422

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '437bb15cc3f4'
down_revision = 'bdd1c2253762'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.Column('role', sa.SmallInteger(), nullable=True),
    sa.Column('job', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('course',
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_course_name'), 'course', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_course_name'), table_name='course')
    op.drop_table('course')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###