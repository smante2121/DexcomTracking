from flask import Flask, render_template, jsonify, session, redirect, url_for, request
import os
from dataRange import DataRange
from egvs import EGVs
from datetime import datetime, timedelta, timezone
import auth
import data
import logging

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

@app.route('/dataRange', methods=["GET"])
def data_range():
    data_range_instance = DataRange()
    data = data_range_instance.get_data()
    if data is not None and 'calibrations' in data:
        return render_template('data_range.html', data_range_data=data)
    else:
        return jsonify({'error': 'Data missing or inaccessible for user'}), 500

def format_datetime_for_dexcom_api(dt):
    return dt.replace(microsecond=0, tzinfo=None).isoformat()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, ssl_context=('cert.pem', 'key.pem'))
