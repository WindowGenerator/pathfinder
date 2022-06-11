"""create dummy users

Revision ID: 14c52a431eb0
Revises: 17610becc1a1
Create Date: 2022-06-12 12:39:01.865584

"""
from alembic import op
from sqlalchemy import Integer, String
from sqlalchemy.sql import column, table

# revision identifiers, used by Alembic.
revision = "14c52a431eb0"
down_revision = "17610becc1a1"
branch_labels = None
depends_on = None


DUMMY_USERS = [
    {
        "email": "test@gmail.ru",
        "username": "Testik_1",
        "hashed_password": "2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b",  # secret
    },
    {
        "email": "bladerunner@android.wo",
        "username": "Droid 1337",
        "hashed_password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # password
    },
    {
        "email": "jojo1@bizzare.adv",
        "username": "Jonathan Joestar",
        "hashed_password": "17f80754644d33ac685b0842a402229adbb43fc9312f7bdf36ba24237a1f1ffb",  # qwerty1234
    },
]

# Create an ad-hoc table to use for the insert statement.
users_table = table(
    "users",
    column("id", Integer),
    column("username", String),
    column("email", String),
    column("hashed_password", String),
)


def upgrade() -> None:
    op.bulk_insert(users_table, DUMMY_USERS)


def downgrade() -> None:
    pass
