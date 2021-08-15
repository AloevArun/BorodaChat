from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Text, nullable=False)
    nickname = Column(String(250), primary_key=True, nullable=False)
    login = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    registration_date = Column(Text, nullable=False)


class MessageTable(Base):
    __tablename__ = 'chats'
    message_id = Column(Text, primary_key=True)
    sender = Column(String(250), nullable=False)
    receiver = Column(String(250), nullable=False)
    message = Column(Text, nullable=False)
    date = Column(Text, nullable=False)
