"""groups model changed

Revision ID: 137a82016418
Revises: a0008c89ccc5
Create Date: 2021-01-31 18:56:44.855797

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '137a82016418'
down_revision = 'a0008c89ccc5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('groups', sa.Column('is_group', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('is_lesson', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('is_level', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('groups', 'is_level')
    op.drop_column('groups', 'is_lesson')
    op.drop_column('groups', 'is_group')
    # ### end Alembic commands ###