import requests
from flask import session

class CalibrationsV3:
    def __init__(self, start_date, end_date):
        self.calibrations = {}
        self.start_date = start_date
        self.end_date = end_date
        self.load_data()

    def load_data(self):
        access_token = session.get('oauth_token', {}).get('access_token')
        if not access_token:
            self.calibrations = {'error': 'Authentication required'}
            return

        #url = "https://sandbox-api.dexcom.com/v3/users/self/calibrations"
        url = "https://api.dexcom.com/v3/users/self/calibrations"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {'startDate': self.start_date, 'endDate': self.end_date}

        try:
            response = requests.get(url, headers=headers, params=params)
            # response = requests.get(deployment_url_v3, headers=headers, params=params)
            response.raise_for_status()  # Ensure HTTP errors are caught
            data = response.json()

            # Transform data here to ensure it matches the Dexcom description
            transformed_data = []
            for record in data.get('records', []):
                transformed_record = {
                    'systemTime': record.get('systemTime'),
                    'displayTime': record.get('displayTime'),
                    'value': record.get('value'),
                    'unit': record.get('unit'),
                    'recordId': record.get('recordId'),
                    'displayDevice': record.get('displayDevice'),
                    'transmitterId': record.get('transmitterId'),
                    'transmitterTicks': record.get('transmitterTicks'),
                    'transmitterGeneration': record.get('transmitterGeneration')
                }
                transformed_data.append(transformed_record)

            self.calibrations = transformed_data
        except requests.exceptions.HTTPError as http_err:
            self.calibrations = {'error': 'HTTP error occurred', 'details': str(http_err), 'response': response.text}
        except requests.exceptions.RequestException as req_err:
            self.calibrations = {'error': 'Failed to retrieve data', 'details': str(req_err)}

    def get_data(self):
        return self.calibrations
