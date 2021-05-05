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

    def all_messages(self):
        msgs = requests.get(f'{self.base_url}/msgs')
        return msgs.json()


if __name__ == '__main__':
    r = HttpClient()
    # print(r.all_messages())
    r.send_message('213142', 'Betal')




# home_response = requests.get(f'{base_url}/')
# add_message = requests.post(f'{base_url}/msg', json=body)
# hello_params = requests.post(f'{base_url}/user/runya/msg/trah')

#
