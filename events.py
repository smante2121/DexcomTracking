import requests
from flask import session

class Events:
    def __init__(self, start_date, end_date):
        self.events = {}
        self.start_date = start_date
        self.end_date = end_date
        self.load_data()

    def load_data(self):
        access_token = session.get('oauth_token', {}).get('access_token')
        if not access_token:
            self.events = {'error': 'Authentication required'}
            return

        url = "https://sandbox-api.dexcom.com/v2/users/self/events"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {'startDate': self.start_date, 'endDate': self.end_date}

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Ensure HTTP errors are caught
            data = response.json()

            # Transform data here to ensure it matches the Dexcom description
            transformed_data = []
            for record in data.get('events', []):
                transformed_record = {
                    'systemTime': record.get('systemTime'),
                    'displayTime': record.get('displayTime'),
                    'eventType': record.get('eventType'),
                    'eventSubType': record.get('eventSubType'),
                    'value': record.get('value'),
                    'unit': record.get('unit'),
                    'eventId': record.get('eventId'),
                    'eventStatus': record.get('eventStatus')
                }
                transformed_data.append(transformed_record)

            self.events = transformed_data
        except requests.exceptions.HTTPError as http_err:
            self.events = {'error': 'HTTP error occurred', 'details': str(http_err), 'response': response.text}
        except requests.exceptions.RequestException as req_err:
            self.events = {'error': 'Failed to retrieve data', 'details': str(req_err)}

    def get_data(self):
        return self.events