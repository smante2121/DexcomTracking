from flask import Flask, jsonify, session
import os
import auth
import data

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config['SESSION_COOKIE_SECURE'] = True

@app.route('/')
def index():
    return auth.login()

@app.route('/callback', methods=["GET"])
def callback():
    return auth.callback()

@app.route('/data')
def data_route():
    return data.get_data()

@app.route('/profile')
def profile():
    user_info = session.get('oauth_token', {}).get('user_info', 'Profile information is not available haha.')
    return f"Profile page of user: {user_info}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, ssl_context=('cert.pem', 'key.pem'))


