from reqs import Reqs
from tkinter import *
# import tkinter as tk
from tkinter import ttk, messagebox
# import threading

# server_url = 'http://127.0.0.1:5000'


if __name__ == '__main__':

    reqs = Reqs()

    def status_window():
            messagebox.showinfo("Status", f"Chat: {reqs.status['chat']}\nUser: {reqs.status['sender']}\nURL: {reqs.status['server_url']}")


    def connect_window():
        def set_addr():
            reqs.status['server_url'] = entry.get()
        cnw = Toplevel()
        cnw.title('Connect')
        label = ttk.Label(cnw, text='Enter server address: ')
        label.grid(row=0, column=0, pady=10, padx=10)
        entry = ttk.Entry(cnw)
        entry.grid(row=0, column=1, pady=10, padx=10)
        con_btn = ttk.Button(cnw, text='Set address', command=set_addr)
        con_btn.grid(row=1, column=1, pady=10, padx=10)
    

    def login():
        def set_user():
            if reqs.login(usr_entry.get()):
                reqs.get_chats()
                chat_name_box.config(state="normal")
                chat_name_box['values'] = reqs.chat_list
                chat_name_box.config(state="readonly")
                lgw.destroy()

        lgw = Toplevel()
        lgw.title('Log in')

        ttk.Label(lgw, text='Log-in').pack(anchor=CENTER, pady=10)
        usr_frame = ttk.LabelFrame(lgw, text='Username', padding=[8, 10])
        pwd_frame = ttk.LabelFrame(lgw, text='Password', padding=[8, 10])
        usr_entry = Entry(usr_frame)
        usr_entry.pack(fill=X, padx=5, pady=5)
        usr_entry.focus()
        pwd_entry = Entry(pwd_frame).pack(fill=X, padx=5, pady=5)
        usr_frame.pack(fill=X, padx=5, pady=5)
        pwd_frame.pack(fill=X, padx=5, pady=5)
        Button(lgw, text='Log-in!', width=10, command=set_user).pack(anchor=CENTER, padx=5, pady=5)

        lgw.focus()
        lgw.resizable(0, 0)

    
    def send():
        txt = message_entry.get("1.0",END)
        message_entry.delete('1.0', END)
        reqs.send(txt, chat_field)

    def open_chat():
        reqs.status['chat'] = chat_name_box.get()
        chat_field.config(state="normal")
        chat_field.delete('1.0', END)
        chat_field.config(state="disabled")
        reqs.print_messages(chat_field, reqs.get_messages())

# --------------------- Setting up UI ---------------------

    root = Tk()
    root.title('Best messenger ever :D')
    root.option_add("*tearOff", FALSE)


    tab_control = ttk.Notebook(root)
    tab_chat = ttk.Frame(tab_control)
    tab_login = ttk.Frame(tab_control)

    tab_control.add(tab_chat, text='Chat')
    tab_control.add(tab_login, text='Log-in')


    # main_menu = Menu()
    # tools_menu = Menu()
    # tools_menu.add_command(label="Status", command=status_window)
    # tools_menu.add_command(label="Connect", command=connect_window)
    # tools_menu.add_command(label="Log in", command=login)
    # main_menu.add_cascade(label='tools', menu=tools_menu)

# --------------------- Chat Tab ---------------------

    open_chat_frame = ttk.LabelFrame(tab_chat, text='Open chat', borderwidth=1, relief=GROOVE, padding=[8, 10])

    open_chat_frame.columnconfigure(index=0, weight=3)
    open_chat_frame.columnconfigure(index=1, weight=1)

    chat_name_box = ttk.Combobox(open_chat_frame, values=reqs.chat_list)
    chat_name_box.grid(row=0, column=0, sticky='ew')
    Button(open_chat_frame, text='Open', command=open_chat).grid(row=0, column=1)
    chat_name_box.config(state="readonly")
    open_chat_frame.pack(anchor=NW, fill=X, padx=5, pady=5)


    chat_frame = ttk.LabelFrame(tab_chat, text='Chat', borderwidth=1, relief=GROOVE, padding=[8, 10])
    text_frame = ttk.Frame(chat_frame)

    chat_field = Text(text_frame, width=40, state=DISABLED, wrap='word')
    chat_field.pack()

    text_frame.pack()


    entry_frame = ttk.Frame(chat_frame)

    message_entry = Text(entry_frame, width=35, height=3)
    send_btn = Button(entry_frame, text='🢅', command=send)
    message_entry.grid(row=0, column=0, padx=5, pady=5)
    send_btn.grid(row=0, column=1, padx=5, pady=5, sticky=NSEW)

    entry_frame.pack()
    chat_frame.pack(padx=5, pady=5)


# --------------------- Log-in Tab ---------------------
    login_frame = ttk.LabelFrame(tab_login, borderwidth=1, relief=GROOVE, padding=[8, 10])
    Button(login_frame, text='Log-in',  command=login, width=10).pack(anchor=CENTER, pady=5)
    Label(login_frame, text='or').pack(anchor=CENTER)
    Button(login_frame, text='Sign-up',  command=login, width=10).pack(anchor=CENTER, pady=5)
    login_frame.pack(padx=5, pady=5, fill=BOTH)
    info_lbl = Label(tab_login, text='Logged in as: ').pack(anchor=W, padx=8+5, pady=10+5)


# --------------------- Start App ---------------------
    tab_control.pack(expand=1, fill="both")
    # root.config(menu=main_menu)
    root.resizable(0,0)
    root.mainloop()