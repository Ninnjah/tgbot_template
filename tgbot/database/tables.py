"""Contains database tables info"""
from datetime import datetime

from sqlalchemy import MetaData, Table, BigInteger, \
    Column, DateTime, String

metadata = MetaData()

users = Table(
    "users", metadata,
    Column("user_id", BigInteger(), primary_key=True),
    Column("firstname", String(), nullable=False),
    Column("lastname", String(), nullable=True),
    Column("fullname", String(), nullable=False),
    Column("username", String(), nullable=True),
    Column("created_on", DateTime(), default=datetime.now),
    Column("updated_on", DateTime(),default=datetime.now, onupdate=datetime.now)
)


admins = Table(
    "admins", metadata,
    Column("user_id", BigInteger(), primary_key=True),
    Column("created_on", DateTime(), default=datetime.now),
    Column("updated_on", DateTime(), default=datetime.now, onupdate=datetime.now)
)
