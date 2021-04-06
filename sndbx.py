import socket


class Connection:
    ip = socket.gethostbyname(socket.gethostname())

    def __init__(self, ip=ip, port='5000'):
        self.ip = ip
        self.port = port

    def set_host(self, ip, port):
        self.ip = ip
        self.port = port

    def get_server_data(self):
        return f'{self.ip}:{self.port}'


class Auth:
    user = 'user'
    password = 'pass'

    def set_auth_data(self, login, password):
        self.user = login
        self.password = password

    def get_auth_data(self):
        return f'{self.user}:{self.password}'


class ConnectionData(Connection, Auth):
    hostname = socket.gethostname()

    def get_all_data(self):
        all_data = dict(hostname=self.hostname,
                        ip=self.ip,
                        port=self.port,
                        user=self.user,
                        password=self.password)
        return all_data


pt = ConnectionData()
# pt.set_host('172.192.6.61', '80')
pt.set_auth_data('ArunAloev', 'Gettherefast')
host = pt.get_all_data()
for i in host.items():
    print(i)
print('\n')
for j in pt.__dict__.items():
    print(j)
print('\n')
print(pt.get_auth_data(), pt.get_server_data())
