import requests


class HttpClient:
    def __init__(self):
        self.base_url = 'http://127.0.0.1:5000'

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

    def check_server(self):
        status = requests.get(f'{self.base_url}/is_online')
        return status.json()

    def registration(self, body: dict):
        response = requests.post(f'{self.base_url}/registration', json=body)
        return response.json()

    def login(self, body: dict):
        response = requests.post(f'{self.base_url}/login', json=body)
        return response.json()

    def get_users(self, login, password):
        body = {
            'login': login,
            'password': password
        }
        response = requests.post(f'{self.base_url}/users', json=body)
        return response.json()


if __name__ == '__main__':
    r = HttpClient()
