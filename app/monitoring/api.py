from flask import Blueprint, render_template, request, jsonify
import requests

# ITSM_REST_API_URL = "http://localhost:8030"
ITSM_REST_API_URL = "http://192.168.10.210:8030"

dashboard_api = Blueprint("monitoring_api", __name__)

@dashboard_api.route("/sensors")
def sensors():
    try:
        url = f"{ITSM_REST_API_URL}/api/v1/sensors/1"
        r = requests.get(url=url)
        return jsonify(r.text)

    except Exception as e:
        # TODO: log and process exception message here
        print("Request error! (sensors) " + str(e))


@dashboard_api.route("/nagios_data")
def nagios_data():
    try:
        # get parameters form GET request
        host_id = request.args.get('host_id', 0, type=int)
        url = f"{ITSM_REST_API_URL}/api/v1/nagios/{host_id}"
        r = requests.get(url=url)
        return jsonify(r.text)

    except Exception as e:
        # TODO: log and process exception message here
        print("Request error! (nagios_data) " + str(e))

@dashboard_api.route("/backups_data")
def backups_data():
    try:
        url = f"{ITSM_REST_API_URL}/api/v1/backups"
        r = requests.get(url=url)
        return jsonify(r.text)

    except Exception as e:
        # TODO: log and process exception message here
        print("Request error! (backups) " + str(e))