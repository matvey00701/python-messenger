import requests
from tkinter import messagebox
from tkinter import Text

class Reqs:

    def __init__(self):

        self.chat_list = []
        self.lastSN = 0

        self.status = {
            'chat': '',
            'sender': '',
            'server_url': 'http://127.0.0.1:5000',
        }

    def send_request(self, route: str, data: dict):
        try:
            response = requests.post(
                self.status['server_url'] + route,
                json=data
            )
            return response.json()
        except:
            messagebox.showerror('Error', f'Something went wrong... :/\nCode: {response.status_code}')

    
    def on_message(message):
        # Handle received message
        print("Received:", message)

    def on_error(error):
        print(error)


    def is_user(self, name):
        data = {'name': name}
        return self.send_request('/is_user', data)['result']


    def login(self, name) -> bool:
        if self.is_user(name):
                self.status['sender'] = name
                return True
        else:
            messagebox.showerror('Error', 'No such user.')
            return False


    def get_chats(self):
        data = {'name': self.status['sender']}
        self.chat_list = self.send_request('/get_chats', data)['result']


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
        return self.send_request('/get_msgs', data)['result']
        

    def send(self, message: str, textbox):
        data = {
            'content': message,
            'conversation': self.status['chat'],
            'sender': self.status['sender'],
            'sn': self.lastSN + 1
        }
        _ = self.send_request('/send', data)['result']
        self.print_messages(textbox, self.get_messages())