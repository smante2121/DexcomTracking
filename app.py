from flask import Flask, redirect, url_for, session, request
from oauthlib.oauth2 import WebApplicationClient
import requests
from requests_oauthlib import OAuth2Session
import os

app = Flask(__name__)



app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')
client_id = 'def'
client_secret = 'abc'
token_url = "https://api.dexcom.com/v2/oauth2/token"
redirect_uri = 'http://localhost:5000/callback'

# Sandbox URLs
authorization_base_url = 'https://sandbox-api.dexcom.com/v2/oauth2/login'
token_url = 'https://sandbox-api.dexcom.com/v2/oauth2/token'
scope = ['offline_access']

# Create an OAuth2 session instance
dexcom = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)

@app.route('/')
def index():
    """Start page with a link to login using Dexcom OAuth."""
    authorization_url, state = dexcom.authorization_url(authorization_base_url, state=os.urandom(16).hex())
    session['oauth_state'] = state  # Save the state in session for later validation
    return f'<a href="{authorization_url}">Log in with Dexcom</a>'

@app.route('/callback')
def callback():
    """Handle the callback from Dexcom after user authorization."""
    dexcom = OAuth2Session(client_id, state=session['oauth_state'], redirect_uri=redirect_uri)
    authorization_response = request.url
    token = dexcom.fetch_token(token_url, client_secret=client_secret, authorization_response=authorization_response)
    session['oauth_token'] = token
    return 'You are logged in with Dexcom!'

def get_access_token(auth_code):
    """Exchange authorization code for an access token."""
    token_url = 'https://sandbox-api.dexcom.com/v2/oauth2/token'
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(token_url, data=data, headers=headers)
    return response.json()

def make_api_request(access_token):
    """Make an API request to Dexcom using the access token."""
    api_url = 'https://sandbox-api.dexcom.com/v2/users/self/egvs'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(api_url, headers=headers)
    return response.json()

def refresh_access_token(refresh_token):
    """Refresh the access token using the refresh token."""
    token_url = 'https://sandbox-api.dexcom.com/v2/oauth2/token'
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(token_url, data=data, headers=headers)
    return response.json()

@app.route('/data')
def get_data():
    """Fetch data from Dexcom API using the stored OAuth token."""
    token = session.get('oauth_token')
    access_token = token['access_token']
    data = make_api_request(access_token)
    return data

if __name__ == '__main__':
    app.run(debug=True)
