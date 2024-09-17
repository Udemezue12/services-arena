"""empty message

Revision ID: 94c1de830f17
Revises: 
Create Date: 2024-09-17 02:20:40.508788

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94c1de830f17'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(length=300), nullable=False),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('password_hash', sa.String(length=200), nullable=False),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('full_name'),
    sa.UniqueConstraint('username')
    )
    op.create_table('complaint',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('provider_name', sa.String(length=100), nullable=True),
    sa.Column('customer_name', sa.String(length=100), nullable=True),
    sa.Column('provider_id', sa.Integer(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('admin_name', sa.String(length=100), nullable=True),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.Column('subject', sa.String(length=150), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('response', sa.Text(), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['customer_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['provider_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=300), nullable=False),
    sa.Column('message', sa.String(length=250), nullable=False),
    sa.Column('read', sa.Boolean(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_name'], ['user.full_name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('service',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('country', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=150), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('state', sa.String(length=100), nullable=True),
    sa.Column('provider_name', sa.String(length=300), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['provider_name'], ['user.full_name'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user__details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.Integer(), nullable=False),
    sa.Column('profile_pic', sa.String(length=200), nullable=True),
    sa.Column('bio', sa.String(length=500), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('certificates', sa.String(length=200), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.Column('phone_number', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['user_name'], ['user.full_name'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_name')
    )
    op.create_table('appointment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=300), nullable=False),
    sa.Column('service_name', sa.String(length=150), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('end_time', sa.Time(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('country', sa.String(length=100), nullable=True),
    sa.Column('state', sa.String(length=100), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['service_name'], ['service.name'], ),
    sa.ForeignKeyConstraint(['user_name'], ['user.full_name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('review',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('service_name', sa.String(length=150), nullable=False),
    sa.Column('reviewer_name', sa.String(length=300), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('comment', sa.String(length=500), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['reviewer_name'], ['user.full_name'], ),
    sa.ForeignKeyConstraint(['service_name'], ['service.name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('review')
    op.drop_table('appointment')
    op.drop_table('user__details')
    op.drop_table('service')
    op.drop_table('notification')
    op.drop_table('complaint')
    op.drop_table('user')
    # ### end Alembic commands ###
