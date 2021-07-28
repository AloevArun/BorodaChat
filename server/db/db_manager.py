import os
import uuid

import arrow
from sqlalchemy import create_engine
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

    # def create_new_dialog_table(self, creator: str, guest: str):
    #     new_table_name = f'{creator}_{guest}'
    #     if new_table_name not in inspector.get_table_names():
    #         ConvMsg.__tablename__ = new_table_name
    #         Table(new_table_name, Base.metadata,
    #               Column('_id', Text, primary_key=True),
    #               Column('user', String(250), nullable=False),
    #               Column('message', Text, nullable=False),
    #               Column('date', Text, nullable=False))
    #
    #         Base.metadata.create_all(engine)
    #         self.add_new_message(creator, '- создал', new_table_name)
    #         return 'Dialog Created'
    #     else:
    #         return 'This dialog already exists'

    def authentification(self, user: str, password: str):
        user = self.session.query(User).filter_by(user=user).one()
        if user['password'] == password:
            auth_status = 'granted'
        else:
            auth_status = 'denied'
        return auth_status

    def user_exists(self, user: str):
        return self.session.query(User).filter_by(user=user).first()

    def add_new_user(self, user: str, password: str):
        if not self.user_exists(user):
            user = User(user_id=uuid.uuid4().hex, user=user, password=password)
            self.session.add(user)
            self.save_to_db()
            return 'User added'
        else:
            return 'User already exists'

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
        for msg in self.session.query(MessageTable).all():
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

#    def delete_user(self, user: str):
#        user_ = self.session.query(User).filter_by(user=user).first()
#        self.session.delete(user_)
#        self.session.commit()
#        self.session.flush()
