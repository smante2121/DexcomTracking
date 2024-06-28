import requests
from flask import session
from datetime import datetime, timedelta

class AlertsV3:
    def __init__(self, start_date, end_date):
        self.alerts = {}
        self.start_date = start_date
        self.end_date = end_date
        self.load_data()

    def load_data(self):
        access_token = session.get('oauth_token', {}).get('access_token')
        if not access_token:
            self.alerts = {'error': 'Authentication required'}
            return

        #url = "https://sandbox-api.dexcom.com/v3/users/self/alerts"
        url= "https://api.dexcom.com/v3/users/self/alerts"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {'startDate': self.start_date, 'endDate': self.end_date}

        try:
            response = requests.get(url, headers=headers, params=params)
            # response = requests.get(url_deployment_v3, headers=headers, params=params)
            response.raise_for_status()  # Ensure HTTP errors are caught
            data = response.json()

            # Transform data here to ensure it matches the Dexcom description
            transformed_data = []
            for record in data.get('records', []):
                transformed_record = {
                    'recordId': record.get('recordId'),
                    'systemTime': record.get('systemTime'),
                    'displayTime': record.get('displayTime'),
                    'alertName': record.get('alertName'),
                    'alertState': record.get('alertState'),
                    'displayDevice': record.get('displayDevice'),
                    'transmitterGeneration': record.get('transmitterGeneration'),
                    'transmitterId': record.get('transmitterId'),
                    'displayApp': record.get('displayApp')
                }
                transformed_data.append(transformed_record)

            self.alerts = transformed_data
        except requests.exceptions.HTTPError as http_err:
            self.alerts = {'error': 'HTTP error occurred', 'details': str(http_err), 'response': response.text}
        except requests.exceptions.RequestException as req_err:
            self.alerts = {'error': 'Failed to retrieve data', 'details': str(req_err)}

    def get_data(self):
        return self.alerts
