"""Add dados table

Revision ID: 93897670635c
Revises: 4dbf53c2a00c
Create Date: 2024-11-07 22:06:33.979474

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '93897670635c'
down_revision = '4dbf53c2a00c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dados',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=120), nullable=False),
    sa.Column('imagens', sa.String(length=200), nullable=True),
    sa.Column('nome_url', sa.String(length=80), nullable=False),
    sa.Column('url', sa.String(length=1000), nullable=False),
    sa.Column('descricao', sa.Text(length=1000), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=40),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.String(length=40),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=False)

    op.drop_table('dados')
    # ### end Alembic commands ###
