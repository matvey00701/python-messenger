import requests
from tkinter import messagebox, Text
import socketio
import threading

class Reqs:

    def __init__(self):

        self.status = {
            'chat': '',
            'sender': '',
            'server_url': 'http://127.0.0.1:5000',
        }

        self.chat_list = []
        self.message_list = []
        self.chat_field = None

        self.sio = socketio.Client()

        @self.sio.event
        def connect():
            print(f"Connected to server with SID: {self.sio.sid}")

        @self.sio.event
        def disconnect():
            print("Disconnected from server")

        @self.sio.on('message')
        def on_message(data):
            print('message!')
            self.update(data)


    def update(self, data: dict):
        convo = data.get('conversation')
        print(data)
        if convo:
            if convo == self.status['chat']:
                self.get_messages()
                self.print_messages()
            else:
                pass


    def run_sw(self):
        self.sio.connect(f'{self.status['server_url']}?client_id={self.status['sender']}', transports=['websocket']) # , query_string={'client_id': client_id})
        self.sio.wait()

    
    def start_sw(self):
        sw_thread = threading.Thread(target=self.run_sw)
        sw_thread.daemon = True
        sw_thread.start()


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

        if self.send_request('/create_convo', data)['result']:
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
            self.start_sw()
            return True


    def login(self, username: str, password: str) -> bool:
        data = {
            'username': username,
            'password': password
        }
        if self.send_request('/login', data)['result']:
            self.status['sender'] = username
            self.start_sw()
            return True


    def get_chats(self):
        data = {'name': self.status['sender']}
        self.chat_list = self.send_request('/get_chats', data)['chats']


    def emit_text(self, text: Text, string: str):
        text.configure(state='normal')
        text.insert('end', string)
        text.configure(state='disabled')


    def print_messages(self):
        self.chat_field.config(state="normal")
        self.chat_field.delete('1.0', 'end')
        self.chat_field.config(state="disabled")
        for message in reversed(self.message_list):
            date = message['date']
            message_string = '─'*40+'\n'
            if message['sender'] == self.status['sender']:
                message_string += f' You                 │ {str(date)}\n'
            else:
                message_string += f' {message['sender']:19} │ {str(date)}\n'
            message_string += ' ' + message['content'] + '\n\n'

            self.emit_text(self.chat_field, message_string)
        self.chat_field.see("end")


    def get_messages(self):
        data = {'conversation': self.status['chat']}
        self.message_list = self.send_request('/get_msgs', data)['messages']
        print(data)
        # return self.send_request('/get_msgs', data)['messages']
        

    def send(self, message: str):
        data = {
            'content': message,
            'conversation': self.status['chat'],
            'sender': self.status['sender'],
        }
        _ = self.send_request('/send', data)
        self.get_messages()
        self.print_messages()