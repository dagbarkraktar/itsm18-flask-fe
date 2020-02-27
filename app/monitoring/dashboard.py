from flask import Blueprint, render_template, request

dashboard_view = Blueprint("monitoring_view", __name__)

@dashboard_view.route("/dashboard")
def dashboard():

    # get layout_id (form GET request)
    layout_id = request.args.get('layout', 0, type=int)

    return render_template("dashboard.html", layout_id=layout_id)