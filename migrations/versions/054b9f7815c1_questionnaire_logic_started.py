"""questionnaire logic started

Revision ID: 054b9f7815c1
Revises: f038c1a527aa
Create Date: 2021-01-26 19:31:32.378147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '054b9f7815c1'
down_revision = 'f038c1a527aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('questionnaires',
    sa.Column('q_id', sa.Integer(), nullable=False),
    sa.Column('q_tags', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('q_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('questionnaires')
    # ### end Alembic commands ###
