import requests
from tkinter import messagebox
from tkinter import Text
# from websocket_stuff import WS

class Reqs:

    def __init__(self):

        self.status = {
            'chat': '',
            'sender': '',
            'server_url': 'http://127.0.0.1:5000',
        }

        self.chat_list = []
        self.lastSN = 0
        # self.ws = WS(self.status['server_url'])


    def send_request(self, route: str, data: dict):
        response = requests.post(
            self.status['server_url'] + route,
            json=data
        )
        if response.json()['result']:
            return response.json()
        messagebox.showerror('Error', f'{response.json()['message']}\nCode: {response.status_code}')

    
    def find_user(self, username: str) -> bool:
        data = {'username': username}
        response = requests.get(
            self.status['server_url'] + '/find_user',
            params=data
        )
        if response.json()['result']:
            return True
        else:
            return False
        
        
    def create_convo(self, username: str) -> bool:
        data = {
            'user1': self.status['sender'],
            'user2': username
        }

        if self.send_request('/create_convo', data):
            return True
        else:
            return False
        
    

    def register(self, username: str, password: str) -> bool:
        data = {
            'username': username,
            'password': password
        }
        if self.send_request('/register', data)['result']:
            self.status['sender'] = username
            return True


    def login(self, username: str, password: str) -> bool:
        data = {
            'username': username,
            'password': password
        }
        if self.send_request('/login', data):
            self.status['sender'] = username
            return True


    def get_chats(self):
        data = {'name': self.status['sender']}
        self.chat_list = self.send_request('/get_chats', data)['chats']


    def emit_text(self, text: Text, string: str):
        text.configure(state='normal')
        text.insert('end', string)
        text.configure(state='disabled')


    def print_messages(self, text, messages: list):
        for message in reversed(messages):
            date = message['date']
            message_string = '─'*40+'\n'
            if message['sender'] == self.status['sender']:
                message_string += f' You                 │ {str(date)}\n'
            else:
                message_string += f' {message['sender']:19} │ {str(date)}\n'
            message_string += ' ' + message['content'] + '\n\n'

            self.emit_text(text, message_string)
        text.see("end")


    def get_messages(self):
        data = {'conversation': self.status['chat']}
        return self.send_request('/get_msgs', data)['messages']
        

    def send(self, message: str, textbox):
        data = {
            'content': message,
            'conversation': self.status['chat'],
            'sender': self.status['sender'],
            'sn': self.lastSN + 1
        }
        _ = self.send_request('/send', data)
        self.print_messages(textbox, self.get_messages())