from flask import Flask, request, jsonify, render_template
from firebase_admin import auth

app = Flask(__name__)

import firebase_admin
from firebase_admin import credentials

# Use a service account
cred = credentials.Certificate('data/quizgenai-firebase.json')
firebase_admin.initialize_app(cred)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    id_token = request.json['idToken']
    print("id_token", id_token)
    try:
        decoded_token = auth.verify_id_token(id_token)
        print("decoded token", decoded_token)
        user = auth.get_user(decoded_token['uid'])
        return jsonify(dict(uid=user.uid, email=user.email, name=user.display_name))
    except Exception as e:
        return jsonify(error=str(e)), 401

if __name__ == '__main__':
    app.run()
