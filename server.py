import time
from datetime import datetime

from flask import Flask, request, abort

app = Flask(__name__)
db = [
    {
        'name': 'Jack',
        'text': 'Hello',
        'time': time.time()
    },
    {
        'name': 'Mary',
        'text': 'Jack',
        'time': time.time()
    },
]

def userCount():
    # функция создает список уникальных юзеров и возвращает его длину
    users = []
    for mes in db:
        username = mes['name']
        if username not in users:
            users.append(username)
    # print(users)
    return len(users)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/status")
def status():
    dt = datetime.now()
    userCount()
    return {
        'status': True,
        'name': 'PyMessenger',
        'time3': time.asctime(),
        'total messages': len(db),
        'users': userCount()
    }


@app.route("/send", methods=['POST'])
def send():
    data = request.json
    if not isinstance(data, dict):
        return abort(400)
    if 'name' not in data or 'text' not in data:
        return abort(400)

    name = data['name']
    text = data['text']

    if not isinstance(name, str) or not isinstance(text, str):
        return abort(400)
    if not 0 < len(name) <= 64:
        return abort(400)
    if not 0 < len(text) <= 10000:
        return abort(400)

    db.append({
        'name': name,
        'text': text,
        'time': time.time()
    })

    return {}


@app.route("/messages")
def messages():
    try:
        after = float(request.args['after'])
    except:
        return abort(400)

    filtered_messages = []

    for message in db:
        if message['time'] > after:
            filtered_messages.append(message)

    return {'messages': filtered_messages[:50]}


app.run()
