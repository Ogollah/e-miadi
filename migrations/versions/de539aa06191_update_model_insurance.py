"""update model insurance

Revision ID: de539aa06191
Revises: 74a7d7d45174
Create Date: 2025-05-26 16:47:07.689946

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de539aa06191'
down_revision = '74a7d7d45174'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('insurance', schema=None) as batch_op:
        batch_op.add_column(sa.Column('provider_name', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('expiry_date', sa.Date(), nullable=False))
        batch_op.alter_column('policy_number',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=120),
               existing_nullable=False)
        batch_op.create_unique_constraint(None, ['policy_number'])
        batch_op.drop_column('coverage_details')
        batch_op.drop_column('company_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('insurance', schema=None) as batch_op:
        batch_op.add_column(sa.Column('company_name', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('coverage_details', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('policy_number',
               existing_type=sa.String(length=120),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
        batch_op.drop_column('expiry_date')
        batch_op.drop_column('provider_name')

    # ### end Alembic commands ###
