"""Creating Gate and Route tables

Revision ID: b6c9ddea4c73
Revises: 
Create Date: 2025-02-05 06:06:49.222279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6c9ddea4c73'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('routes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('source_gate_id', sa.String(length=3), nullable=False),
    sa.Column('destination_gate_id', sa.String(length=3), nullable=False),
    sa.Column('hyperplane_units', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['destination_gate_id'], ['gate.id'], ),
    sa.ForeignKeyConstraint(['source_gate_id'], ['gate.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('gate', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('gate', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)

    op.drop_table('routes')
    # ### end Alembic commands ###
