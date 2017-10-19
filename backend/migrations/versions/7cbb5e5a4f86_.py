"""empty message

Revision ID: 7cbb5e5a4f86
Revises: 
Create Date: 2017-09-28 22:52:13.097928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7cbb5e5a4f86'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('schedule',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start', sa.DateTime(), nullable=False),
    sa.Column('end', sa.DateTime(), nullable=False),
    sa.Column('purpouse', sa.String(length=45), nullable=False),
    sa.Column('i_can_enter', sa.Boolean(), nullable=False),
    sa.Column('weeks_day', sa.String(length=45), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('security_key',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('security_key', sa.String(length=90), nullable=False),
    sa.PrimaryKeyConstraint('id', 'security_key'),
    sa.UniqueConstraint('security_key')
    )
    op.create_table('event_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('event', sa.String(length=45), nullable=False),
    sa.Column('key', sa.String(length=90), nullable=False),
    sa.ForeignKeyConstraint(['key'], ['security_key.security_key'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('internal_id', sa.Integer(), nullable=True),
    sa.Column('key', sa.String(length=90), nullable=False),
    sa.Column('name', sa.String(length=90), nullable=False),
    sa.Column('profession', sa.String(length=45), nullable=False),
    sa.ForeignKeyConstraint(['key'], ['security_key.security_key'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('key')
    )
    op.create_table('laboratory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('laboratory')
    op.drop_table('user')
    op.drop_table('event_log')
    op.drop_table('security_key')
    op.drop_table('schedule')
    # ### end Alembic commands ###