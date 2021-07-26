import os

import arrow
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    _id = Column(Integer, primary_key=True)
    user = Column(String(250), nullable=False)
    password = Column(Text, nullable=False)


class Message(Base):
    __tablename__ = 'message'
    _id = Column(Integer, primary_key=True)
    user = Column(String(250), nullable=False)
    message = Column(Text, nullable=False)
    date = Column(Text, nullable=False)


class DBManager:
    def __init__(self):
        self.session = None
        self._create_session()

    def _create_session(self):
        database_path = 'db/main.db'
        engine = create_engine(f'sqlite:///{database_path}?check_same_thread=False')

        if not os.path.exists(database_path):
            Base.metadata.create_all(engine)
        else:
            Base.metadata.bind = engine

        self.session = sessionmaker(bind=engine)()

    def authentification(self, user: str, password: str):
        user = self.session.query(User).filter_by(user=user).one()
        if user['password'] == password:
            auth_status = 'granted'
        else:
            auth_status = 'denied'
        return auth_status

    def user_exists(self, user: str):
        user_exists = False
        for users in self.session.query(User).all():
            usr = {'user': users.user}
            if user == usr:
                user_exists = True
            else:
                user_exists = False
        return user_exists

    def add_new_user(self, user: str, password: str):
        if not self.user_exists(user):
            _id = len(self.session.query(User).all()) + 1
            user = User(_id=_id, user=user, password=password)
            self.session.add(user)
            self.session.commit()
            self.session.flush()
            return True
        else:
            return False

    def delete_user(self, user: str):
        user_ = self.session.query(User).filter_by(user=user).first()
        self.session.delete(user_)
        self.session.commit()
        self.session.flush()

    def add_new_message(self, user: str, text: str):
        _id = len(self.session.query(Message).all()) + 1
        date = arrow.now().format('YYYY-MM-DDTh:m:s.SS')
        msg = Message(_id=_id, user=user, message=text, date=date)
        self.session.add(msg)
        self.session.commit()
        self.session.flush()

    def read_all_messages(self):
        all_messages = []
        for msg in self.session.query(Message).all():
            message = {
                'user': msg.user,
                'message': msg.message,
                'time': msg.date
            }
            all_messages.append(message)
        self.session.flush()
        return all_messages

    def read_new_messages(self, time: str):
        new_messages = []
        for msg in self.session.query(Message).all():
            message = {
                'user': msg.user,
                'message': msg.message,
                'time': msg.date
            }

            fmt = 'YYYY-MM-DDTh:m:s.SS'
            client_message_time = arrow.get(message['time'], fmt)
            last_db_message_time = arrow.get(time, fmt)
            if client_message_time > last_db_message_time:
                new_messages.append(message)
        self.session.flush()
        return new_messages
