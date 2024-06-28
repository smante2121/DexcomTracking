import os
import requests
from flask import session, redirect, url_for, request, jsonify
from requests_oauthlib import OAuth2Session

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')
authorization_base_url = 'https://sandbox-api.dexcom.com/v2/oauth2/login'
token_url = 'https://sandbox-api.dexcom.com/v2/oauth2/token'
#deployment_base_url_v2='https://api.dexcom.com/v2/oauth2/login'
#deployment_token_url_v2='https://api.dexcom.com/v2/oauth2/token'
#deployment_base_url_v3='https://api.dexcom.com/v3/oauth2/login'
#deployment_token_url_v3='https://api.dexcom.com/v3/oauth2/token'

def login():
    dexcom = OAuth2Session(client_id, scope="offline_access", redirect_uri=redirect_uri)
    authorization_url, state = dexcom.authorization_url(authorization_base_url)
    #authorization_url, state = dexcom.authorization_url(eployment_base_url_v2)
    #authorization_url, state = dexcom.authorization_url(eployment_base_url_v3)
    session['oauth_state'] = state
    return redirect(authorization_url)

def callback():
    if 'oauth_state' not in session:
        return redirect(url_for('index'))

    dexcom = OAuth2Session(client_id, state=session['oauth_state'], redirect_uri=redirect_uri)
    authorization_response = request.url
    try:
        data = {
            'grant_type': 'authorization_code',
            'code': request.args.get('code'),
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(token_url, data=data, headers=headers)
        #response = requests.post(deployment_token_url_v2, data=data, headers=headers)
        #response = requests.post(deployment_token_url_v3, data=data, headers=headers)
        response.raise_for_status()
        token = response.json()
        session['oauth_token'] = token
        return redirect(url_for('profile'))
    except Exception as e:
        return jsonify({'error': 'Failed to fetch token', 'description': str(e)}), 500

def refresh_access_token(refresh_token):
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        response = requests.post(token_url, data=data, headers=headers)
        #response = requests.post(deployment_token_url_v2, data=data, headers=headers)
        #response = requests.post(deployment_token_url_v3, data=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}
