"""empty message

Revision ID: 6967ad519472
Revises: 
Create Date: 2024-08-18 20:13:17.358775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6967ad519472'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('twitch_id', sa.BigInteger(), nullable=False),
    sa.Column('twitch_login', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_twitch_id'), 'users', ['twitch_id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_twitch_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
