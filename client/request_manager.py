import requests


class HttpClient:
    def __init__(self):
        self.base_url = 'http://127.0.0.1:5000'

    def send_message(self, message: str, user: str):
        body = {
            'text': message,
            'user': user,
        }
        requests.post(f'{self.base_url}/msg', json=body)

    def update_messages(self, time: str):
        body = {'time': time}
        new_msgs = requests.post(f'{self.base_url}/whats_new', json=body)
        return new_msgs.json()

    def get_all_messages(self, user: str, password: str):
        body = {'user': user,
                'password': password}
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


if __name__ == '__main__':
    r = HttpClient()
    print(r.get_all_messages())
