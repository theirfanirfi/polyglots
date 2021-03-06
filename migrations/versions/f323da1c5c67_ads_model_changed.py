"""ads model changed

Revision ID: f323da1c5c67
Revises: a4f84135ca43
Create Date: 2021-01-28 14:47:36.295347

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f323da1c5c67'
down_revision = 'a4f84135ca43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('advertisements', sa.Column('ad_age', sa.Integer(), nullable=False))
    op.drop_column('advertisements', 'ad_age_lower_limit')
    op.drop_column('advertisements', 'ad_age_upper_limit')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('advertisements', sa.Column('ad_age_upper_limit', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.add_column('advertisements', sa.Column('ad_age_lower_limit', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.drop_column('advertisements', 'ad_age')
    # ### end Alembic commands ###
