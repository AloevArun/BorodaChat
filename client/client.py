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

    def get_all_messages(self):
        msgs = requests.get(f'{self.base_url}/msgs')
        return msgs.json()

    def check_server(self):
        status = requests.get(f'{self.base_url}/is_online')
        return status.json()

    def registration(self, body: dict):
        response = requests.post('', json=body)
        return response.json()


if __name__ == '__main__':
    r = HttpClient()
    print(r.get_all_messages())


#
