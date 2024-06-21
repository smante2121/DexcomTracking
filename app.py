import logging

import requests
from flask import Flask, redirect, url_for, session, request, jsonify
from requests_oauthlib import OAuth2Session
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')
authorization_base_url = 'https://sandbox-api.dexcom.com/v2/oauth2/login'
token_url = 'https://sandbox-api.dexcom.com/v2/oauth2/token'
app.config['SESSION_COOKIE_SECURE'] = True



@app.route('/')
def index():
    """Step 2: User Authorization.
    Redirect the user/resource owner to the OAuth provider (i.e. Dexcom)
    using an URL with a few key OAuth parameters.
    """
    dexcom = OAuth2Session(client_id, scope="offline_access", redirect_uri=redirect_uri)
    authorization_url, state = dexcom.authorization_url(authorization_base_url)
    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    print(f"Authorization URL: {authorization_url}")
    print(f"State: {state}")
    return redirect(authorization_url)



@app.route('/callback', methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.
    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """
    if 'oauth_state' not in session:
        return redirect(url_for('.index'))
    dexcom = OAuth2Session(client_id, state=session['oauth_state'], redirect_uri=redirect_uri)
    authorization_response = request.url
    print(f"Authorization response: {authorization_response}")  # Debug print
    try:
        # Prepare the data payload according to the Dexcom documentation
        data = {
            'grant_type': 'authorization_code',
            'code': request.args.get('code'),
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        print(f"Payload: {data}")  # Debug print

        # Make the POST request to the token URL
        response = requests.post(token_url, data=data, headers=headers)
        token = response.json()
        print(f"Token response: {token}")  # Debug print

        # Store the token in the session
        session['oauth_token'] = token
        return redirect(url_for('.profile'))
    except Exception as e:
        print(f"Error in fetching token: {e}")  # Debug print
        return jsonify({'error': 'Failed to fetch token', 'description': str(e)}), 500

def make_api_request(access_token, start_date, end_date):
    """Make an API request to Dexcom using the access token."""
    api_url = 'https://sandbox-api.dexcom.com/v2/users/self/egvs'
    headers = {'Authorization': f'Bearer {access_token}'}
    query = {
        "startDate": start_date,
        "endDate": end_date
    }
    try:
        print(f"Request: GET {api_url} with headers {headers} and query {query}")  # Debug print
        response = requests.get(api_url, headers=headers, params=query)
        response.raise_for_status()  # Raises HTTPError for bad responses
        data = response.json()
        print(f"Response: {data}")  # Debug print
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return {'error': str(e)}


@app.route('/data')
def get_data():
    """Fetch data from Dexcom API using the stored OAuth token."""
    token = session.get('oauth_token', {})
    if not token:
        return jsonify({'error': 'No token found'}), 401
    access_token = token.get('access_token')
    if not access_token:
        token = refresh_access_token(token.get('refresh_token'))
        if 'access_token' in token:
            session['oauth_token'] = token  # Update the session with the new token
            access_token = token['access_token']
        else:
            return jsonify({'error': 'Failed to refresh token'}), 401
    start_date = "2023-01-01T09:12:35"  # Replace with your start date
    end_date = "2023-01-01T09:12:35"  # Replace with your end date
    response = make_api_request(access_token, start_date, end_date)
    if 'error' in response:
        return jsonify(response), 500
    return jsonify(response)




def refresh_access_token(refresh_token):
    """Refresh the access token using the refresh token."""
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        print(f"Request: POST {token_url} with headers {headers} and data {data}")  # Debug print
        response = requests.post(token_url, data=data, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses
        token = response.json()
        print(f"Response: {token}")  # Debug print
        return token
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return {}



@app.route('/refresh', methods=["GET"])
def refresh():
    """Refreshing an OAuth 2 token."""
    token = session.get('oauth_token', {})
    if not token:
        return jsonify({'error': 'No token found'}), 401
    refresh_token = token.get('refresh_token')
    if not refresh_token:
        return jsonify({'error': 'No refresh token found'}), 401
    new_token = refresh_access_token(refresh_token)
    if 'access_token' in new_token:
        session['oauth_token'] = new_token  # Update the session with the new token
        return jsonify({'message': 'Token refreshed successfully'})
    else:
        return jsonify({'error': 'Failed to refresh token'}), 500



@app.route('/profile')
def profile():
    # Assuming 'oauth_token' is stored in the session and contains user information
    user_info = session.get('oauth_token', {}).get('user_info', 'sophia')
    return f"Profile page of user: {user_info}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, ssl_context=('cert.pem', 'key.pem'))
