from flask import Flask, redirect, url_for, session, request
from oauthlib.oauth2 import WebApplicationClient
import requests
from requests_oauthlib import OAuth2Session
import os

app = Flask(__name__)

#app.secret_key = 'Sophia'  # Needed for session management
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')


CLIENT_ID = 'abc'
CLIENT_SECRET = 'def'
REDIRECT_URI = 'http://localhost:5000/callback'
#AUTHORIZATION_BASE_URL = 'https://sandbox-api.dexcom.com/v3/oauth2/login' # Updated for V3
#TOKEN_URL = 'https://sandbox-api.dexcom.com/v3/oauth2/token' # Updated for V3
AUTHORIZATION_BASE_URL = 'https://sandbox-api.dexcom.com/v2/oauth2/login'
TOKEN_URL = 'https://sandbox-api.dexcom.com/v2/oauth2/token'

# Define the necessary scopes
SCOPES = ['offline_access']


@app.route('/')
def index():
    """Start page with a link to login using Dexcom OAuth."""
    return '<a href="/login">Log in with Dexcom</a>'

@app.route('/login')
def login():
    """Redirect to Dexcom for user to authorize our app."""
    dexcom = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPES)
    #authorization_url, _ = dexcom.authorization_url(AUTHORIZATION_BASE_URL)
    authorization_url, state = dexcom.authorization_url(AUTHORIZATION_BASE_URL, state=os.urandom(16).hex())
    #authorization_url, state = dexcom.authorization_url(AUTHORIZATION_BASE_URL,
                                                       # response_type='code',
                                                        #state=session.get('oauth_state'))
    session['oauth_state'] = state  # Save the state in session for later validation
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    """Handle the callback from Dexcom after user authorization."""
    #dexcom = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    dexcom = OAuth2Session(CLIENT_ID, state=session['oauth_state'], redirect_uri=REDIRECT_URI)
    token = dexcom.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=request.url)
    session['oauth_token'] = token
    return 'You are logged in with Dexcom!'

@app.route('/data')
def get_data():
    """Fetch data from Dexcom API using the stored OAuth token."""
    dexcom = OAuth2Session(CLIENT_ID, token=session['oauth_token'])
    #response = dexcom.get('https://sandbox-api.dexcom.com/your-api-endpoint')
    response = dexcom.get('https://sandbox-api.dexcom.com/v2/users/self/dataRange')
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
