from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# from app.models import hwdb
from models import hwdb

# Get creds from env
MYSQL_ITSM18_USER = os.environ.get("MYSQL_ITSM18_USER") or "MYSQL_USER"
MYSQL_ITSM18_PASS = os.environ.get("MYSQL_ITSM18_PASS") or "MYSQL_PASS"
MYSQL_ITSM18_HOST = os.environ.get("MYSQL_ITSM18_HOST") or "127.0.0.1"

app = Flask(__name__)

# TODO: Move mysql creds to config
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY') or 'SOME SECRET KEY'
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://{MYSQL_ITSM18_USER}:{MYSQL_ITSM18_PASS}@{MYSQL_ITSM18_HOST}/itsm18"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# import & register blueprints
from monitoring.dashboard import dashboard_view
from monitoring.api import dashboard_api
from hardware.maintenance import hwdb_maintenance
from hardware.hw_list import hwdb_list

app.register_blueprint(dashboard_view)
app.register_blueprint(dashboard_api)
app.register_blueprint(hwdb_maintenance)
app.register_blueprint(hwdb_list)


if __name__ == "__main__":
    app.run(host="", port=8040, debug=False)
