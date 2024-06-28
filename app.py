from flask import Flask, render_template, jsonify
import os
from v2.calibrations import Calibrations
from v2.dataRange import DataRange
from v2.devices import Devices
from v2.egvs import EGVs
from datetime import datetime, timedelta, timezone
import auth
import data
from v2.events import Events
# from v3.devices_v3 import DevicesV3
# from v3.events_v3 import EventsV3
#from v3.calibrations_v3 import CalibrationsV3
# from v3.egvs_v3 import EGVsV3
# from v3.data_range_v3 import DataRangeV3
# from v3.alerts_v3 import AlertsV3

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config['SESSION_COOKIE_SECURE'] = True

@app.route('/')
def index():
    return auth.login()
    #return render_template('index.html')

@app.route('/profile')
def profile():

    return render_template('index.html')
    #return render_template('index_v3.html')

@app.route('/callback', methods=["GET"])
def callback():
    return auth.callback()

@app.route('/data')
def data_route():
    return data.get_data()

@app.route('/egvs', methods=["GET"])
def egvs_route():
    try:
        start_date = format_datetime_for_dexcom_api(datetime.now(timezone.utc) - timedelta(days=1))
        end_date = format_datetime_for_dexcom_api(datetime.now(timezone.utc))
        egvs_instance = EGVs(start_date, end_date)
        data = egvs_instance.get_data()
        if 'error' in data:
            return jsonify(data), 500
        return render_template('egvs.html', egvs_data=data)
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
    # Uncomment the following block to use v3 EGVs
    # try:
    #     egvs_instance_v3 = EGVsV3(start_date, end_date)
    #     data = egvs_instance_v3.get_data()
    #     if 'error' in data:
    #         return jsonify(data), 500
    #     return render_template('egvs_v3.html', egvs_data=data)
    # except Exception as e:
    #     return jsonify({'error': 'Internal server error', 'details': str(e)}), 500



@app.route('/events', methods=["GET"])
def events():
    try:
        start_date = format_datetime_for_dexcom_api(datetime.now(timezone.utc) - timedelta(days=1))
        end_date = format_datetime_for_dexcom_api(datetime.now(timezone.utc))
        events_instance = Events(start_date, end_date)
        data = events_instance.get_data()
        if 'error' in data:
            return jsonify(data), 500
        return render_template('events.html', events_data=data)
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
    # Uncomment the following block to use v3 events
    # try:
    #     events_instance_v3 = EventsV3(start_date, end_date)
    #     data = events_instance_v3.get_data()
    #     if 'error' in data:
    #         return jsonify(data), 500
    #     return render_template('events_v3.html', events_data=data)
    # except Exception as e:
    #     return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@app.route('/devices', methods=["GET"])
def devices():
    try:
        start_date = format_datetime_for_dexcom_api(datetime.now(timezone.utc) - timedelta(days=1))
        end_date = format_datetime_for_dexcom_api(datetime.now(timezone.utc))
        devices_instance = Devices(start_date, end_date)
        data = devices_instance.get_data()
        if 'error' in data:
            return jsonify(data), 500
        return render_template('devices.html', devices_data=data)
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
    # Uncomment the following block to use v3 devices
    # try:
    #     devices_instance_v3 = DevicesV3()
    #     data = devices_instance_v3.get_data()
    #     if 'error' in data:
    #         return jsonify(data), 500
    #     return render_template('devices_v3.html', devices_data=data)
    # except Exception as e:
    #     return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@app.route('/calibrations', methods=["GET"])
def calibrations():
    try:
        start_date = format_datetime_for_dexcom_api(datetime.now(timezone.utc) - timedelta(days=1))
        end_date = format_datetime_for_dexcom_api(datetime.now(timezone.utc))
        calibrations_instance = Calibrations(start_date, end_date)
        data = calibrations_instance.get_data()
        if 'error' in data:
            return jsonify(data), 500
        return render_template('calibrations.html', calibrations_data=data)
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
    # Uncomment the following block to use v3 calibrations
    # try:
    #     calibrations_instance_v3 = CalibrationsV3(start_date, end_date)
    #     data = calibrations_instance_v3.get_data()
    #     if 'error' in data:
    #         return jsonify(data), 500
    #     return render_template('calibrations_v3.html', calibrations_data=data)
    # except Exception as e:
    #     return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@app.route('/dataRange', methods=["GET"])
def data_range():
    data_range_instance = DataRange()
    data = data_range_instance.get_data()
    if data is not None and 'calibrations' in data:
        return render_template('data_range.html', data_range_data=data)
    else:
        return jsonify({'error': 'Data missing or inaccessible for user'}), 500
    # Uncomment the following block to use v3 dataRange
    # try:
    #     last_sync_time = request.args.get('lastSyncTime')
    #     data_range_instance_v3 = DataRangeV3(last_sync_time)
    #     data = data_range_instance_v3.get_data()
    #     if 'error' in data:
    #         return jsonify(data), 500
    #     return render_template('data_range_v3.html', data_range_data=data)
    # except Exception as e:
    #     return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


#@app.route('/alerts', methods=["GET"])
#def alerts_route():
    #try:
        #start_date = format_datetime_for_dexcom_api(datetime.now(timezone.utc) - timedelta(days=1))
        #end_date = format_datetime_for_dexcom_api(datetime.now(timezone.utc))
        #alerts_instance = AlertsV3(start_date, end_date)
        #data = alerts_instance.get_data()
        #if 'error' in data:
            #return jsonify(data), 500
        #return render_template('alerts_v3.html', alerts_data=data)
    #except Exception as e:
        #return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


def format_datetime_for_dexcom_api(dt):
    return dt.replace(microsecond=0, tzinfo=None).isoformat()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, ssl_context=('cert.pem', 'key.pem'))
