from Reqs import Reqs
from tkinter import *
from tkinter import ttk, messagebox
import threading

# server_url = 'http://127.0.0.1:5000'


if __name__ == '__main__':
    reqs = Reqs()

    def status_window():
            messagebox.showinfo("Status", f"Chat: {reqs.status['chat']}\n\
User: {reqs.status['sender']}\n\
URL: {reqs.status['server_url']}")


    def connect_window():
        def set_addr():
            reqs.status['server_url'] = entry.get()
        cnw = Toplevel()
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
            if reqs.login(entry.get()):
                reqs.get_chats()
                chat_name_box.config(state="normal")
                chat_name_box['values'] = reqs.chat_list
                chat_name_box.config(state="readonly")
                lgw.destroy()

        lgw = Tk()
        lgw.title('Log in')
        label = ttk.Label(lgw, text='Enter your username: ')
        label.grid(row=0, column=0, pady=10, padx=10)
        entry = ttk.Entry(lgw)
        entry.grid(row=0, column=1, pady=10, padx=10)
        con_btn = ttk.Button(lgw, text='Set user', command=set_user)
        con_btn.grid(row=1, column=1, pady=10, padx=10)
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


    root = Tk()
    root.title('Best messenger ever :D')
    root.option_add("*tearOff", FALSE)


    main_menu = Menu()
    tools_menu = Menu()
    tools_menu.add_command(label="Status", command=status_window)
    tools_menu.add_command(label="Connect", command=connect_window)
    tools_menu.add_command(label="Log in", command=login)
    main_menu.add_cascade(label='tools', menu=tools_menu)

    open_chat_frame = ttk.LabelFrame(text='Open chat', borderwidth=1, relief=GROOVE, padding=[8, 10])

    open_chat_frame.columnconfigure(index=0, weight=3)
    open_chat_frame.columnconfigure(index=1, weight=1)

    chat_name_box = ttk.Combobox(open_chat_frame, values=reqs.chat_list)
    chat_name_box.grid(row=0, column=0, sticky='ew')
    Button(open_chat_frame, text='Open', command=open_chat).grid(row=0, column=1)
    chat_name_box.config(state="readonly")
    open_chat_frame.pack(anchor=NW, fill=X, padx=5, pady=5)


    chat_frame = ttk.LabelFrame(text='Chat', borderwidth=1, relief=GROOVE, padding=[8, 10])


    text_frame = ttk.Frame(chat_frame)

    chat_field = Text(text_frame, width=40, state=DISABLED, wrap='word')
    chat_field.pack()

    text_frame.pack()


    entry_frame = ttk.Frame(chat_frame)

    message_entry = Text(entry_frame, width=35, height=3)
    message_entry.grid(row=0, column=0, padx=5, pady=5)

    send_btn = Button(entry_frame, text='🢅', command=send)
    send_btn.grid(row=0, column=1, padx=5, pady=5, sticky=NSEW)

    entry_frame.pack()


    chat_frame.pack(padx=5, pady=5)

    root.config(menu=main_menu)
    root.resizable(0,0)
    root.mainloop()