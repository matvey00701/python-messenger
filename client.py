from reqs import Reqs
from tkinter import *
from tkinter import ttk, messagebox
import time
import threading


if __name__ == '__main__':

    reqs = Reqs()

    def status_window():
            messagebox.showinfo("Status", f"Chat: {reqs.status['chat']}\nUser: {reqs.status['sender']}\nURL: {reqs.status['server_url']}")

    def update_chat():
        while True:
            reqs.get_messages()
            reqs.print_messages(chat_field)
            time.sleep(1)

    def register():
        def command():
            username = usr_entry.get()
            password = pwd_entry.get()

            if reqs.register(username=username, password=password):
                reqs.get_chats()
                chat_name_box.config(state="normal")
                chat_name_box['values'] = reqs.chat_list
                chat_name_box.config(state="readonly")
                lgw.destroy()

        lgw = Toplevel()
        lgw.title('Register')

        ttk.Label(lgw, text='Register').pack(anchor=CENTER, pady=10)
        usr_frame = ttk.LabelFrame(lgw, text='Username', padding=[8, 10])
        pwd_frame = ttk.LabelFrame(lgw, text='Password', padding=[8, 10])
        usr_entry = Entry(usr_frame)
        usr_entry.pack(fill=X, padx=5, pady=5)
        usr_entry.focus()
        pwd_entry = Entry(pwd_frame, show='●')
        pwd_entry.pack(fill=X, padx=5, pady=5)
        usr_frame.pack(fill=X, padx=5, pady=5)
        pwd_frame.pack(fill=X, padx=5, pady=5)
        Button(lgw, text='Register!', width=10, command=command).pack(anchor=CENTER, padx=5, pady=5)

        lgw.focus()
        lgw.resizable(0, 0)
    

    def login():
        def set_user():
            if reqs.login(usr_entry.get(), pwd_entry.get()):
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
        pwd_entry = Entry(pwd_frame, show='●')
        pwd_entry.pack(fill=X, padx=5, pady=5)
        usr_frame.pack(fill=X, padx=5, pady=5)
        pwd_frame.pack(fill=X, padx=5, pady=5)
        Button(lgw, text='Log-in!', width=10, command=set_user).pack(anchor=CENTER, padx=5, pady=5)

        lgw.focus()
        lgw.resizable(0, 0)


    def send():
        txt = message_entry.get("1.0",END)
        message_entry.delete('1.0', END)
        reqs.send(txt)


    def open_chat():
        reqs.status['chat'] = chat_name_box.get()
        reqs.get_messages()
        reqs.print_messages()


# --------------------- Setting up UI ---------------------

    root = Tk()
    root.title('Silliest messenger ever :D')
    root.option_add("*tearOff", FALSE)


    tab_control = ttk.Notebook(root)
    tab_chat = ttk.Frame(tab_control)
    tab_find = ttk.Frame(tab_control)

    tab_control.add(tab_chat, text='Chat')
    tab_control.add(tab_find, text='Find')

# --------------------- Top Menu ---------------------

    main_menu = Menu()
    tools_menu = Menu()
    login_menu = Menu()
    tools_menu.add_command(label="Status", command=status_window)
    login_menu.add_command(label='Log-in', command=login)
    login_menu.add_command(label='Register', command=register)
    main_menu.add_cascade(label='tools', menu=tools_menu)
    main_menu.add_cascade(label='Log-in', menu=login_menu)

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
    reqs.chat_field = chat_field

    text_frame.pack()


    entry_frame = ttk.Frame(chat_frame)

    message_entry = Text(entry_frame, width=35, height=3)
    send_btn = Button(entry_frame, text='🢅', command=send)
    message_entry.grid(row=0, column=0, padx=5, pady=5)
    send_btn.grid(row=0, column=1, padx=5, pady=5, sticky=NSEW)

    entry_frame.pack()
    chat_frame.pack(padx=5, pady=5)

# --------------------- Find Tab ---------------------
    def find_user(*args):
        if reqs.find_user(username.get()):

            inf_lbl.configure(text=f'User {username.get()} found!')
        else:
            inf_lbl.configure(text=f'User {username.get()} not found')

    def messageto():
        if reqs.create_convo(username.get()):
            reqs.get_chats()
            chat_name_box.config(state="normal")
            chat_name_box['values'] = reqs.chat_list
            chat_name_box.config(state="readonly")


    find_frame = ttk.LabelFrame(tab_find, text='Username', borderwidth=1, padding=[8, 10])
    find_frame.pack(fill='both', padx=5, pady=5)
    username = StringVar()
    username.trace_add('write', find_user)
    usr_entry = Entry(find_frame, textvariable=username)
    inf_lbl = ttk.Label(find_frame, text=' ')

    # packing
    usr_entry.pack(anchor='center', padx=5, pady=5, fill=X)
    inf_lbl.pack(anchor='center', pady=5)
    Button(find_frame, text='Message to', command=messageto, width=10).pack(anchor='center', pady=5)


# --------------------- Start App ---------------------
    tab_control.pack(expand=1, fill="both")
    root.config(menu=main_menu)
    root.resizable(0,0)
    root.mainloop()