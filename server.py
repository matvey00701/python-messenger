# In dev!

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask, request, abort, jsonify

app = Flask(__name__)
cred = credentials.Certificate('messenger-for-uni-06332e181228.json')

fs_app = firebase_admin.initialize_app(cred)
db = firestore.client()


connected_users = {}

# @socketio.on('connect')
# def handle_connect():
#     user_id = request.args.get('user_id')  # Assuming user ID is passed as a query parameter
#     connected_users[user_id] = request.sid
#     print(f"User {user_id} connected.")

# @socketio.on('disconnect')
# def handle_disconnect():
#     user_id = None
#     for uid, sid in connected_users.items():
#         if sid == request.sid:
#             user_id = uid
#             del connected_users[uid]
#             break
#     if user_id:
#         print(f"User {user_id} disconnected.")
        

# def send_message_to_user(user_id, message):
#     if user_id in connected_users:
#         socketio.emit('message', message, room=connected_users[user_id])
#     else:
#         print(f"User {user_id} is not connected.")


@app.route("/")
def hello():
    return "What the hella you doin' here??"


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

    return jsonify({'result': chats})


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
    return jsonify({'result': lst})
    


@app.route("/get_msgs", methods=['POST'])
def get_msgs():
    conv = request.get_json()['conversation']
    msgs = db.collection('messages')\
        .where('conversation_id', '==', str(conv))\
        .order_by('timestamp', direction=firestore.Query.DESCENDING)\
        .limit(50)\
        .get()

    return jsonify_messages(msgs)


# def send_update(client_id, message_data):
#     if client_id in client_connections:
#         connection = client_connections[client_id]
#         connection.send(message_data)


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

    members = db.collection('conversations').document(convID).get().to_dict().get('members')
    for member in members:
        if member != sender_name:
            # send_message_to_user(member, 'hi :)')
            pass
        else:
            pass

    try:
        # Add message data to Firestore
        db.collection("messages").add(message_data)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



app.run()