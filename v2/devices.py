import requests
from flask import session

class Devices:
    def __init__(self, start_date, end_date):
        self.devices = {}
        self.start_date = start_date
        self.end_date = end_date
        self.load_data()

    def load_data(self):
        access_token = session.get('oauth_token', {}).get('access_token')
        if not access_token:
            self.devices = {'error': 'Authentication required'}
            return

        url = "https://sandbox-api.dexcom.com/v2/users/self/devices"
        #url_deployment_v2 = "https://api.dexcom.com/v2/users/self/devices"
        #url_deployment_v3 = "https://api.dexcom.com/v3/users/self/devices"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {'startDate': self.start_date, 'endDate': self.end_date}

        try:
            response = requests.get(url, headers=headers, params=params)
            #response = requests.get(url_deployment_v2, headers=headers, params=params)
            #response = requests.get(url_deployment_v3, headers=headers, params=params)
            response.raise_for_status()  # Ensure HTTP errors are caught
            data = response.json()

            # Transform data here to ensure it matches the Dexcom description
            transformed_data = []
            for record in data.get('devices', []):
                transformed_record = {
                    'transmitterGeneration': record.get('transmitterGeneration'),
                    'displayDevice': record.get('displayDevice'),
                    'lastUploadDate': record.get('lastUploadDate'),
                    'alertScheduleList': record.get('alertScheduleList', []),
                    'alertSettings': record.get('alertSettings', [])
                }
                transformed_data.append(transformed_record)

            self.devices = transformed_data
        except requests.exceptions.HTTPError as http_err:
            self.devices = {'error': 'HTTP error occurred', 'details': str(http_err), 'response': response.text}
        except requests.exceptions.RequestException as req_err:
            self.devices = {'error': 'Failed to retrieve data', 'details': str(req_err)}

    def get_data(self):
        return self.devices