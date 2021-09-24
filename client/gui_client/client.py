import requests


class Host:
    base_url = 'http://127.0.0.1:5000'

    def set_host(self, ip: str, port: str):
        self.base_url = f'http://{ip}:{port}'


class HttpClient(Host):

    def check_server(self):
        try:
            status = requests.get(f'{self.base_url}/is_online')
        except requests.exceptions.ConnectionError:
            raise ConnectionError
        else:
            return status.json()

    def login(self, body: dict):
        response = requests.post(f'{self.base_url}/login', json=body)
        return response.json()

    def registration(self, body: dict):
        response = requests.post(f'{self.base_url}/registration', json=body)
        return response.json()

    def get_users(self, login, password):
        body = {
            'login': login,
            'password': password
        }
        response = requests.post(f'{self.base_url}/users', json=body)
        return response.json()

    def send_message(self, login, password, receiver, text):
        body = {
            'login': login,
            'password': password,
            'receiver': receiver,
            'text': text
        }
        requests.post(f'{self.base_url}/add_message', json=body)

    def get_messages(self, login: str, password: str, time='0001-01-01T00:00:00.00'):
        body = {'login': login,
                'password': password,
                'time': time}
        msgs = requests.post(f'{self.base_url}/messages', json=body)
        return msgs.json()


if __name__ == '__main__':
    host = HttpClient()
    host.set_host('127.0.0.1', '5000')
    print(host.check_server())
    print(host.base_url)
    host.set_host('127.0.0.1', '5000342')
    print(host.base_url)
