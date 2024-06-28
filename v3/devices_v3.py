import requests
from flask import session

class DevicesV3:
    def __init__(self):
        self.devices = {}
        self.load_data()

    def load_data(self):
        access_token = session.get('oauth_token', {}).get('access_token')
        if not access_token:
            self.devices = {'error': 'Authentication required'}
            return

        #url = "https://sandbox-api.dexcom.com/v3/users/self/devices"
        url = "https://api.dexcom.com/v3/users/self/devices"
        headers = {"Authorization": f"Bearer {access_token}"}

        try:
            response = requests.get(url, headers=headers)
            # response = requests.get(url_deployment_v3, headers=headers)
            response.raise_for_status()  # Ensure HTTP errors are caught
            data = response.json()

            # Transform data here to ensure it matches the Dexcom description
            transformed_data = []
            for record in data.get('records', []):
                transformed_record = {
                    'transmitterGeneration': record.get('transmitterGeneration'),
                    'displayDevice': record.get('displayDevice'),
                    'lastUploadDate': record.get('lastUploadDate'),
                    'alertSchedules': [{
                        'alertScheduleName': schedule.get('alertScheduleName'),
                        'isEnabled': schedule.get('isEnabled'),
                        'isDefaultSchedule': schedule.get('isDefaultSchedule'),
                        'startTime': schedule.get('startTime'),
                        'endTime': schedule.get('endTime'),
                        'daysOfWeek': schedule.get('daysOfWeek'),
                        'isActive': schedule.get('isActive'),
                        'override': schedule.get('override'),
                        'alertSettings': [{
                            'alertName': setting.get('alertName'),
                            'value': setting.get('value'),
                            'unit': setting.get('unit'),
                            'snooze': setting.get('snooze'),
                            'enabled': setting.get('enabled'),
                            'systemTime': setting.get('systemTime'),
                            'displayTime': setting.get('displayTime'),
                            'delay': setting.get('delay'),
                            'secondaryTriggerCondition': setting.get('secondaryTriggerCondition'),
                            'soundTheme': setting.get('soundTheme'),
                            'soundOutputMode': setting.get('soundOutputMode')
                        } for setting in schedule.get('alertSettings', [])]
                    } for schedule in record.get('alertSchedules', [])]
                }
                transformed_data.append(transformed_record)

            self.devices = transformed_data
        except requests.exceptions.HTTPError as http_err:
            self.devices = {'error': 'HTTP error occurred', 'details': str(http_err), 'response': response.text}
        except requests.exceptions.RequestException as req_err:
            self.devices = {'error': 'Failed to retrieve data', 'details': str(req_err)}

    def get_data(self):
        return self.devices
