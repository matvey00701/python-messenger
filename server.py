# In dev!

import time
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask, request, abort, jsonify

app = Flask(__name__)
cred = credentials.Certificate('messenger-for-uni-06332e181228.json')

fs_app = firebase_admin.initialize_app(cred)
db = firestore.client()


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/send", methods=['POST'])
def send():
    data = request.get_json()

    content = data.get('content')
    convID = data.get('conversation')
    sender_name = data.get('sender')
    timestamp = firestore.SERVER_TIMESTAMP

    if not content or not convID or not sender_name:
        return abort(400)
    
    # usr = db.collection('users').where('nickname', '==', str(sender_name)).get()
    print(content + '; ' + convID + '; ' + sender_name)
    
    message_data = {
        "content": content,
        "conversation_id": convID,
        "sender": str(sender_name),
        "timestamp": timestamp
    }
    try:
        # Add message data to Firestore
        db.collection("messages").add(message_data)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



app.run()