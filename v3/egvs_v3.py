import requests
from flask import session
from datetime import datetime, timedelta


class EGVsV3:
    def __init__(self, start_date, end_date):
        self.egvs = {}
        self.start_date = start_date
        self.end_date = end_date
        self.load_data()

    def load_data(self):
        access_token = session.get('oauth_token', {}).get('access_token')
        if not access_token:
            self.egvs = {'error': 'Authentication required'}
            return

        #url = "https://sandbox-api.dexcom.com/v3/users/self/egvs"
        url = "https://api.dexcom.com/v3/users/self/egvs"
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
                    'transmitterId': record.get('transmitterId'),
                    'transmitterTicks': record.get('transmitterTicks'),
                    'value': record.get('value'),
                    'status': record.get('status'),
                    'trend': record.get('trend'),
                    'trendRate': record.get('trendRate'),
                    'unit': record.get('unit'),
                    'rateUnit': record.get('rateUnit'),
                    'displayDevice': record.get('displayDevice'),
                    'transmitterGeneration': record.get('transmitterGeneration')
                }
                transformed_data.append(transformed_record)

            self.egvs = transformed_data
        except requests.exceptions.HTTPError as http_err:
            self.egvs = {'error': 'HTTP error occurred', 'details': str(http_err), 'response': response.text}
        except requests.exceptions.RequestException as req_err:
            self.egvs = {'error': 'Failed to retrieve data', 'details': str(req_err)}

    def get_data(self):
        return self.egvs
