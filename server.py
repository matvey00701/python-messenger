import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask, request, abort, jsonify
from flask_socketio import SocketIO
import bcrypt


app = Flask(__name__)
sio = SocketIO(app, async_mode='gevent')
cred = credentials.Certificate('messenger-for-uni-06332e181228.json')

fs_app = firebase_admin.initialize_app(cred)
db = firestore.client()


clients = {}


def send_to_client(client, data):
    client_sid = clients.get(client)
    if client_sid:
        sio.emit('message', data, room=client_sid)
        print(f'message sent to {client}')


@sio.on('connect')
def on_connect():
    client_id = request.args.get('client_id')
    if client_id:
        clients[client_id] = request.sid
        print(f'Client {client_id} connected with SID {request.sid}')


@sio.on('disconnect')
def on_disconnect():
    client_id = None
    for cid, sid in clients.items():
        if sid == request.sid:
            client_id = cid
            break
    if client_id:
        del clients[client_id]
        print(f'Client {client_id} disconnected')


@app.route('/clients', methods=['POST'])
def snd_clients():
    return jsonify(clients), 200


@app.route('/create_convo', methods=['POST'])
def create_convo():
    data = request.json
    usr1 = data['user1']
    usr2 = data['user2']

    convo_name = f'{usr1}-{usr2}'
    A = db.collection('conversations').document(convo_name).get()
    if A.exists:
        return jsonify({'result': False, 'message': 'Chat already exists.'}), 418
    B = db.collection('conversations').document(f'{usr2}-{usr1}').get()
    if B.exists:
        return jsonify({'result': False, 'message': 'Chat already exists.'}), 418

    db.collection('conversations').add(document_id=convo_name, document_data={'members': [usr1, usr2]})
    return jsonify({'result': True, 'chat_name': convo_name}), 200


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password'].encode('utf-8')

    user = db.collection('users').document(username).get()

    if not user.exists:
        # Hash the password with bcrypt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)

        db.collection('users').add(document_id=username, document_data={
            'display_name': username,
            'password': hashed_password.decode('utf-8')
        })

        return jsonify({'result': True}), 201
    return jsonify({'result': False, 'message': 'User already exists.'}), 418


@app.route('/login', methods=['POST'])
def login():
    data = request.json

    username = data['username']
    password = data['password'].encode('utf-8')

    # Retrieve the user from Firestore
    user = db.collection('users').document(username).get()

    if not user.exists:
        return jsonify({'result': False, 'message': 'Invalid username'}), 401

    stored_hashed_password = user.get('password').encode('utf-8')

    # Verify the password
    if bcrypt.checkpw(password, stored_hashed_password):
        return jsonify({'result': True, 'message': 'Login successful'}), 200
    else:
        return jsonify({'result': False, 'message': 'Invalid username or password'}), 401


@app.route("/find_user", methods=['GET'])
def find_user():
    username = request.args.get('username')
    if not username:
        return jsonify({'result': False, 'message': 'Username is required'}), 400
    
    user = db.collection('users').document(username).get()

    if not user.exists:
        return jsonify({'result': False, 'message': 'User was not found :((('}), 404
    
    return jsonify({'result': True}), 200
    


@app.route("/")
def hello():
    return "yeah"


@app.route("/is_user", methods=['POST'])
def is_user():
    name = request.get_json()['name']
    usr = db.collection('users').document(str(name)).get()
    if usr.exists:
        return jsonify({'result': True})
    else:
        return jsonify({'result': False})
    

@app.route("/get_chats", methods=['POST'])
def get_chats():
    name = request.get_json()['name']

    chats = db.collection('conversations').where('members', 'array_contains', str(name)).get()

    for i, chat in enumerate(chats):
        chats[i] = chat.id

    return jsonify({'result': True, 'chats': chats})


def jsonify_messages(msg_lst: list):
    lst = []
    for msg in msg_lst:
        msg_content = msg.get('content')
        msg_sender = msg.get('sender')
        msg_date = msg.get('timestamp').strftime("%d.%m.%Y %H:%M")

        lst.append(
            {
                'content': msg_content,
                'sender': msg_sender,
                'date': msg_date,
            }
        )
    return jsonify({'result': True, 'messages': lst})
    


@app.route("/get_msgs", methods=['POST'])
def get_msgs():
    conv = request.get_json()['conversation']
    msgs = db.collection('messages')\
        .where('conversation_id', '==', str(conv))\
        .order_by('timestamp', direction=firestore.Query.DESCENDING)\
        .limit(50)\
        .get()

    return jsonify_messages(msgs)


@app.route("/send", methods=['POST'])
def send():
    data = request.get_json()

    content = data.get('content')
    convID = data.get('conversation')
    sender_name = data.get('sender')
    timestamp = firestore.SERVER_TIMESTAMP

    if not content or not convID or not sender_name:
        return abort(400)

    message_data = {
        "content": content,
        "conversation_id": convID,
        "sender": str(sender_name),
        "timestamp": timestamp
    }

    try:
        # Add message data to Firestore
        db.collection("messages").add(message_data)
        members = db.collection('conversations').document(convID).get().to_dict().get('members')
        for member in members:
            if member != sender_name:
                if member in clients:
                    send_to_client(member, data)
            else:
                pass
        return jsonify({'result': True}), 200
    except Exception as e:
        print(e)
        return jsonify({'result': False}), 500


sio.run(app)