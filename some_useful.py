#    def delete_user(self, user: str):
#        user_ = self.session.query(UserTable).filter_by(user=user).first()
#        self.session.delete(user_)
#        self.session.commit()
#        self.session.flush()

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


# @app.route('/delete_user', methods=['POST'])
# def delete_user():
#     body = request.get_json()
#     user = body['user']
#     db.delete_user(user)
#     return body


def resize_window(self):
    if self.auth_tab.isActiveWindow():
        AuthWindow.resize(370, 740)
    elif self.regist_tab.isActiveWindow():
        AuthWindow.resize(370, 380)