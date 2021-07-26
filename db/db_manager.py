import os

import arrow
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


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
        table_path = 'db/message_table.db'
        engine = create_engine(f'sqlite:///{table_path}?check_same_thread=False')

        if not os.path.exists(table_path):
            Base.metadata.create_all(engine)
        else:
            Base.metadata.bind = engine

        self.session = sessionmaker(bind=engine)()

    def add(self, user: str, text: str):
        _id = len(self.session.query(Message).all()) + 1
        date = arrow.now().format('YYYY-MM-DDTh:m:s.SS')
        msg = Message(_id=_id, user=user, message=text, date=date)
        self.session.add(msg)
        self.session.commit()
        self.session.flush()

    def read_all(self):
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

    def read_new(self, time: str):
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
