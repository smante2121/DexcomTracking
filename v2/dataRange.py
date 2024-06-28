import requests
from flask import session, jsonify

class DataRange:
    def __init__(self):
        self.data_range = {}
        self.load_data()

    def load_data(self):
        access_token = session.get('oauth_token', {}).get('access_token')
        if not access_token:
            self.data_range = {'error': 'Authentication required'}
            return


        url = "https://sandbox-api.dexcom.com/v2/users/self/dataRange"
        #deployment_url_v2 = "https://api.dexcom.com/v2/users/self/dataRange"
        #deployment_url_v3 = "https://api.dexcom.com/v3/users/self/dataRange"
        headers = {"Authorization": f"Bearer {access_token}"}

        try:
            response = requests.get(url, headers=headers)
            #response = requests.get(deployment_url_v2, headers=headers)
            #response = requests.get(deployment_url_v3, headers=headers)
            response.raise_for_status()
            self.data_range = response.json()
        except requests.exceptions.HTTPError as http_err:
            self.data_range = {'error': 'HTTP error occurred', 'details': str(http_err)}
        except requests.exceptions.RequestException as req_err:
            self.data_range = {'error': 'Failed to retrieve data', 'details': str(req_err)}

    def get_data(self):
        return self.data_range

# Example usage
# data_range_instance = DataRange()
# data_range = data_range_instance.get_data()
# print(data_range)