import os
import uuid

import arrow
from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker

from .tables import User, MessageTable, Base


class DBManager:
    def __init__(self):

        self.session = None
        self.database_path = 'db/main.db'
        self.engine = create_engine(f'sqlite:///{self.database_path}?check_same_thread=False')
        self._create_session()

    def _create_session(self):
        if not os.path.exists(self.database_path):
            Base.metadata.create_all(self.engine)
        else:
            Base.metadata.bind = self.engine

        self.session = sessionmaker(bind=self.engine)()

    def authentication(self, user_name: str, password: str):
        user = self.user_exists(user_name)
        if user and user.password == password:
            return {'nickname': user.nickname}

    def user_exists(self, user_name: str):
        try:
            result = self.session.query(User).filter_by(nickname=user_name).one()
        except NoResultFound as ex:
            return None
        else:
            return result

    def nickname_exists(self, nickname: str):
        return self.session.query(User).filter_by(nickname=nickname).first()

    def add_new_user(self, nickname: str, user_name: str, password: str):
        if self.user_exists(user_name):
            return 'user_exists'

        elif self.nickname_exists(nickname):
            return 'Nick is not available'

        date = arrow.now().format('YYYY-MM-DDTh:m:s.SS')
        user = User(user_id=uuid.uuid4().hex, nickname=nickname, login=user_name, password=password,
                    registration_date=date)
        self.session.add(user)
        self.save_to_db()
        return 'added'

    def save_to_db(self):
        self.session.commit()
        self.session.flush()

    def add_new_message(self, sender: str, receiver: str, text: str):
        date = arrow.now().format('YYYY-MM-DDTh:m:s.SS')

        msg = MessageTable(
            message_id=uuid.uuid4().hex,
            sender=sender,
            receiver=receiver,
            message=text,
            date=date
        )

        self.session.add(msg)
        self.save_to_db()

    def read_all_messages(self):
        all_messages = []
        for msg in self.session.query(MessageTable).all():
            message = {
                'sender': msg.sender,
                'receiver': msg.receiver,
                'message': msg.message,
                'time': msg.date
            }
            all_messages.append(message)
        self.session.flush()
        return all_messages

    def read_new_messages(self, time: str):
        new_messages = []
        all_messages = self.session.query(MessageTable).all()
        if len(all_messages) != 0:
            for msg in all_messages:
                message = {
                    'sender': msg.sender,
                    'receiver': msg.receiver,
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
