from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer, BLOB

from utils.conn import Base


def create_db():
    Base.metadata.create_all()


class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(10), unique=True)
    create_time = Column(DateTime, default=datetime.now)
    __tablename__ = 'user'
