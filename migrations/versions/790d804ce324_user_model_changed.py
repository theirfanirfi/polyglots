"""user model changed

Revision ID: 790d804ce324
Revises: 137a82016418
Create Date: 2021-01-31 22:08:23.023134

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '790d804ce324'
down_revision = '137a82016418'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmation_code', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('continent', sa.Integer(), nullable=False))
    op.add_column('users', sa.Column('country', sa.Integer(), nullable=False))
    op.add_column('users', sa.Column('is_confirmed', sa.Integer(), nullable=True))
    op.drop_column('users', 'continent_id')
    op.drop_column('users', 'country_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('country_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.add_column('users', sa.Column('continent_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.drop_column('users', 'is_confirmed')
    op.drop_column('users', 'country')
    op.drop_column('users', 'continent')
    op.drop_column('users', 'confirmation_code')
    # ### end Alembic commands ###
