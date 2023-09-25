"""01_initial-db

Revision ID: ee2976e30c5e
Revises:
Create Date: 2023-09-20 10:54:20.562957

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ee2976e30c5e"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "links",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("url_full", sa.String(), nullable=True),
        sa.Column("url_short", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "actions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("link_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["link_id"],
            ["links.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("actions")
    op.drop_table("links")
    # ### end Alembic commands ###
