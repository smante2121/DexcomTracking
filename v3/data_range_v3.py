import requests
from flask import session

class DataRangeV3:
    def __init__(self, last_sync_time=None):
        self.data_range = {}
        self.last_sync_time = last_sync_time
        self.load_data()

    def load_data(self):
        access_token = session.get('oauth_token', {}).get('access_token')
        if not access_token:
            self.data_range = {'error': 'Authentication required'}
            return

        url = "https://sandbox-api.dexcom.com/v3/users/self/dataRange"
        # url_deployment_v3 = "https://api.dexcom.com/v3/users/self/dataRange"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {}
        if self.last_sync_time:
            params['lastSyncTime'] = self.last_sync_time

        try:
            response = requests.get(url, headers=headers, params=params)
            # response = requests.get(url_deployment_v3, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            self.data_range = {
                'recordType': data.get('recordType'),
                'recordVersion': data.get('recordVersion'),
                'userId': data.get('userId'),
                'calibrations': data.get('calibrations', {}),
                'egvs': data.get('egvs', {}),
                'events': data.get('events', {})
            }
        except requests.exceptions.HTTPError as http_err:
            self.data_range = {'error': 'HTTP error occurred', 'details': str(http_err), 'response': response.text}
        except requests.exceptions.RequestException as req_err:
            self.data_range = {'error': 'Failed to retrieve data', 'details': str(req_err)}

    def get_data(self):
        return self.data_range
