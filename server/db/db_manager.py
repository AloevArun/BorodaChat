import os
import uuid
import arrow

from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker

from .tables import UserTable, MessageTable, Base


class DBManager:
    def __init__(self):
        super().__init__()
        self.Message = self
        self.User = self
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

    def save_to_db(self):
        self.session.commit()
        self.session.flush()


class User(DBManager):

    def login(self, login: str, password: str):
        user = self.user_exists(login)
        return {'response': user.nickname} if user and user.password == password else {'response': 'denied'}

    def create(self, nickname: str, user_name: str, password: str):
        if self.user_exists(user_name):
            return {'response': 'user_exists'}

        elif self.nickname_exists(nickname):
            return {'response': 'nickname_exists'}
        else:
            date = arrow.now().format('YYYY-MM-DDTh:m:s.SS')
            user = UserTable(user_id=uuid.uuid4().hex, nickname=nickname, login=user_name, password=password,
                             registration_date=date)
            self.session.add(user)
            self.save_to_db()
            return {'response': 'added'}

    def user_exists(self, login: str):
        try:
            result = self.session.query(UserTable).filter_by(login=login).first()
        except NoResultFound:
            return None
        else:
            return result

    def nickname_exists(self, nickname: str):
        return self.session.query(UserTable).filter_by(nickname=nickname).first()

    def get_all(self):
        users = []
        for user in self.session.query(UserTable.nickname):
            users.append(''.join(user))
        return users


class Message(DBManager):

    def add(self, sender: str, receiver: str, text: str):
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

    def read(self, time):
        messages = []
        for msg in self.session.query(MessageTable).all():
            message = {
                'sender': msg.sender,
                'receiver': msg.receiver,
                'message': msg.message,
                'time': msg.date
            }

            fmt = 'YYYY-MM-DDTh:m:s.SS'
            if arrow.get(message['time'], fmt) > arrow.get(time, fmt):
                messages.append(message)

        self.session.flush()
        return messages

#    def delete(self, user: str, time: str):
#        message = self.session.query(MessageTable).filter_by(date=time).first()
#        message_to_del = MessageTable(
#            message_id=message.message_id,
#            sender=message.sender,
#            receiver=message.receiver,
#            message=message.message,
#            date=message.date
#        )
#        if message:
#            if message.sender == user:
#                self.session.query(MessageTable).delete(message_to_del)
#                return 'done'
#            else:
#                return 'wrong_sender'
#        else:
#            return 'message_not_exists'
