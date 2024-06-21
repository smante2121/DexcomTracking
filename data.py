import requests
import logging
import auth
from flask import jsonify, session

def make_api_request(access_token, start_date, end_date):
    api_url = 'https://sandbox-api.dexcom.com/v2/users/self/egvs'
    headers = {'Authorization': f'Bearer {access_token}'}
    query = {"startDate": start_date, "endDate": end_date}
    try:
        response = requests.get(api_url, headers=headers, params=query)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return {'error': str(e)}

def get_data():
    token = session.get('oauth_token', {})
    if not token:
        return jsonify({'error': 'No token found'}), 401
    access_token = token.get('access_token')
    if not access_token:
        access_token_info = auth.refresh_access_token(token.get('refresh_token'))
        access_token = access_token_info.get('access_token')
        if not access_token:
            return jsonify({'error': 'Failed to refresh token'}), 401
        session['oauth_token'] = access_token_info  # Update the session with the new token
    start_date = "2023-01-01T09:12:35"  # Example start date
    end_date = "2023-01-01T09:12:35"  # Example end date
    response = make_api_request(access_token, start_date, end_date)
    if 'error' in response:
        return jsonify(response), 500
    return jsonify(response)
