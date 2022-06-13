"""init

Revision ID: 9d667a7fae28
Revises: 
Create Date: 2022-06-13 00:28:40.899797

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9d667a7fae28'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("""CREATE SEQUENCE coordinates_number_seq;""")

    op.create_table('coordinates',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('x_coord', sa.Integer(), nullable=False),
    sa.Column('y_coord', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), server_default=sa.text("nextval('coordinates_number_seq')"), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('x_coord', 'y_coord', name='chk_coordinates_x_coord_y_coord')
    )
    op.create_index('idx_coordinates_x_coord_y_coord', 'coordinates', ['x_coord', 'y_coord'], unique=False)
    op.create_table('routes',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_by_user_with_id', sa.Integer(), nullable=False),
    sa.Column('route_order', postgresql.ARRAY(postgresql.UUID(as_uuid=True), as_tuple=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('routes_coordinates',
    sa.Column('route_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('coordinate_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['coordinate_id'], ['coordinates.id'], ),
    sa.ForeignKeyConstraint(['route_id'], ['routes.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('routes_coordinates')
    op.drop_table('routes')
    op.drop_index('idx_coordinates_x_coord_y_coord', table_name='coordinates')
    op.drop_table('coordinates')
    # ### end Alembic commands ###
