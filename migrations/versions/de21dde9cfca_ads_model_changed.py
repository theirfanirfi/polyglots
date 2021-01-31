"""ads model changed

Revision ID: de21dde9cfca
Revises: f323da1c5c67
Create Date: 2021-01-31 15:30:06.500114

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'de21dde9cfca'
down_revision = 'f323da1c5c67'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('advertisements', sa.Column('is_bottom_ad', sa.Integer(), nullable=True))
    op.alter_column('users', 'age',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('users', 'continent_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('users', 'country_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('users', 'gender',
               existing_type=mysql.VARCHAR(length=15),
               nullable=False,
               existing_server_default=sa.text("''"))
    op.alter_column('users', 'token',
               existing_type=mysql.VARCHAR(length=200),
               nullable=False,
               existing_server_default=sa.text("''"))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'token',
               existing_type=mysql.VARCHAR(length=200),
               nullable=True,
               existing_server_default=sa.text("''"))
    op.alter_column('users', 'gender',
               existing_type=mysql.VARCHAR(length=15),
               nullable=True,
               existing_server_default=sa.text("''"))
    op.alter_column('users', 'country_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('users', 'continent_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('users', 'age',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.drop_column('advertisements', 'is_bottom_ad')
    # ### end Alembic commands ###