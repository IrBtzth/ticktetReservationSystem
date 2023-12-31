"""empty message

Revision ID: ac4f1a6996fb
Revises: 
Create Date: 2023-06-14 15:12:38.770575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac4f1a6996fb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trains', schema=None) as batch_op:
        batch_op.alter_column('fcSeat',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.Integer(),
               existing_nullable=False)
        batch_op.alter_column('scSeat',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.Integer(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trains', schema=None) as batch_op:
        batch_op.alter_column('scSeat',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)
        batch_op.alter_column('fcSeat',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)

    # ### end Alembic commands ###
