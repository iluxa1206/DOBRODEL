import datetime

import sqlalchemy

from .database_session import SqlAlchemyBase
from sqlalchemy import orm


class Meeting(SqlAlchemyBase):
    __tablename__ = "meetings"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    tema = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    leader = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("users.id"),
                               nullable=False)
    members = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    user = orm.relation("User")
