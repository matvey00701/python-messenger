import requests
import sys
import os
from tkinter import *
from tkinter import ttk, messagebox

# server_url = 'http://127.0.0.1:5000'

# functions
class Cli:

    def __init__(self):
        self.commands = {
            '/login': self.login,
            '/exit': self.exit_app,
            '/open-chat': self.open_chat,
            '/status': self.print_status
        }

        self.status = {
            'chat': 'dev2-dev_account',
            'sender': '',
            'server_url': 'http://127.0.0.1:5000'
        }

    
    def login(self):
        nickname = input('Enter your nickname: ')
        self.status['sender'] = str(nickname)

    def exit_app(self):
        sys.exit()

    def open_chat(self):
        os.system('cls')
        print('TODO: open covos\n')

    def parseCommand(self, command):
        if command in self.commands:
            self.commands[command]()
        else:
            print("Wrong command :/")

    def print_status(self):
        os.system('cls')
        print(self.status)

    def send(self, message: str, chat: str, user: str):
        data = {
            'content': message,
            'conversation': chat,
            'sender': user
        }
    
        try:
            response = requests.post(
                self.status['server_url'] + '/send',
                json=data
            )
        except:
            print("Error, unable to send a message :(")

    def engine(self):
        # while True:
        #     usr_input = input()
        #     if usr_input[0] == '/':
        #         self.parseCommand(str(usr_input))
        #     else:
        #         if self.status['chat'] == '' or self.status['sender'] == '':
        #             print("you're not loged in or didn't chose chat")
        #         else:
        #             self.send(str(usr_input), self.status['chat'], self.status['sender'])
        pass


if __name__ == '__main__':
    cli = Cli()

    def status_window():
            messagebox.showinfo("Status", f"Chat: {cli.status['chat']}\n\
User: {cli.status['sender']}\n\
URL: {cli.status['server_url']}")


    def connect_window():
        def set_addr():
            cli.status['server_url'] = entry.get()
        cnw = Tk()
        cnw.title('Connect')
        # cnw.geometry('200x100')
        label = ttk.Label(cnw, text='Enter server address: ')
        label.grid(row=0, column=0, pady=10, padx=10)
        entry = ttk.Entry(cnw)
        entry.grid(row=0, column=1, pady=10, padx=10)
        con_btn = ttk.Button(cnw, text='Set address', command=set_addr)
        con_btn.grid(row=1, column=1, pady=10, padx=10)
    

    def login():
        def set_user():
            cli.status['sender'] = entry.get()


        lgw = Tk()
        lgw.title('Log in')
        # lgw.geometry('200x100')
        label = ttk.Label(lgw, text='Enter your username: ')
        label.grid(row=0, column=0, pady=10, padx=10)
        entry = ttk.Entry(lgw)
        entry.grid(row=0, column=1, pady=10, padx=10)
        con_btn = ttk.Button(lgw, text='Set user', command=set_user)
        con_btn.grid(row=1, column=1, pady=10, padx=10)

    
    def insert():
        txt = message_entry.get("1.0",END)
        message_entry.delete('1.0', END)
        chat_field.configure(state=NORMAL)
        chat_field.insert('end', txt)
        chat_field.configure(state=DISABLED)


    root = Tk()
    root.title('Best messenger ever :D')
    # root.geometry("307x437")
    root.option_add("*tearOff", FALSE)


    main_menu = Menu()
    tools_menu = Menu()
    tools_menu.add_command(label="Status", command=status_window)
    tools_menu.add_command(label="Connect", command=connect_window)
    tools_menu.add_command(label="Log in", command=login)
    main_menu.add_cascade(label='tools', menu=tools_menu)


    chats = ['dev2-dev_account', 'Me-You', 'Aris-Momoi']

    open_chat_frame = ttk.Frame(borderwidth=1, relief=GROOVE, padding=[8, 10])

    for c in range(2): open_chat_frame.columnconfigure(index=c, weight=1)

    Label(open_chat_frame, text='Open chat').grid(row=0, column=0)
    chat_name_box = ttk.Combobox(open_chat_frame, values=chats)
    chat_name_box.grid(row=0, column=1)
    Button(open_chat_frame, text='Open').grid(row=0, column=2)

    open_chat_frame.pack(anchor=NW, fill=X, padx=5, pady=5)


    # label = Label(text='TODO: Make the rest of the app...')
    # label.pack()

    chat_frame = ttk.Frame(borderwidth=1, relief=GROOVE, padding=[8, 10])


    text_frame = ttk.Frame(chat_frame)

    chat_field = Text(text_frame, width=40, state=DISABLED)
    chat_field.pack()

    text_frame.pack()


    entry_frame = ttk.Frame(chat_frame)

    message_entry = Text(entry_frame, width=35, height=3)
    message_entry.grid(row=0, column=0, padx=5, pady=5)

    send_btn = Button(entry_frame, text='🢅', command=insert)
    send_btn.grid(row=0, column=1, padx=5, pady=5, sticky=NSEW)

    entry_frame.pack()


    chat_frame.pack(padx=5, pady=5)

    root.config(menu=main_menu)
    root.resizable(0,0)
    root.mainloop()