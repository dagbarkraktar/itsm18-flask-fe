from flask import Blueprint, render_template, redirect, url_for, request, session

from models import hwdb
from main import db

# TODO: move to settings/env
# current year (for maintenance)
CURRENT_YEAR = 2020

hwdb_maintenance = Blueprint("hwdb_maintenance", __name__)


@hwdb_maintenance.route("/maintenance_docs", methods=['GET', ])
def maintenance_docs():
    """
    Render maintenance documents list for selected year
    :return: render template maintenance_docs.html
    """
    # get year (form GET request)
    selected_year = request.args.get('year', 0, type=int)
    maintenance_records_qty = 0

    # if received year is incorrect
    if (selected_year == 0) or (selected_year < 2017) or (selected_year > CURRENT_YEAR):
        # set year (from session or default)
        if "selected_year" in session:
            selected_year = session.get("selected_year")
        else:
            selected_year = CURRENT_YEAR
            session["selected_year"] = CURRENT_YEAR

    # {"maintenance_id": units_quantity}
    units_qty_dict = {}

    try:
        # Get maintenance docs list from db
        mt_list = db.session.query(hwdb.MaintenanceDocsDbModel)\
            .filter(hwdb.MaintenanceDocsDbModel.year == selected_year)\
            .order_by(hwdb.MaintenanceDocsDbModel.id).all()

        # TODO: Fix this o_O
        # Get quantity of hw units in each maintenance docs (by counting last_maintenance_id in hwdb table)
        for mntc in mt_list:
            units_qty_dict[mntc.id] = db.session.query(hwdb.HwDbModel)\
                                        .filter(hwdb.HwDbModel.last_maintenance_id == mntc.id).count()

        # TODO: Fix wrong counting (add smth like current_year field)
        # get record quantity
        maintenance_records_qty = db.session.query(hwdb.MaintenanceDbModel).count()

    except Exception as e:
        # TODO: Add logging
        print(f"Database error: {e}")
        mt_list = []

    return render_template("maintenance_docs.html", mt_list=mt_list, rec_qty=maintenance_records_qty, qty_dict=units_qty_dict)


@hwdb_maintenance.route("/maintenance", methods=['GET', ])
def maintenance():
    """
    Add unit maintenance info to DB
    :return: redirect back to hardware list
    """

    # get unit id (form GET request)
    hw_unit_id = request.args.get('hw_id', 0, type=int)

    try:
        # get current maintenance_doc (last added)
        maintenance_doc = db.session.query(hwdb.MaintenanceDocsDbModel) \
            .order_by(hwdb.MaintenanceDocsDbModel.id.desc()).first()

        # save maintenance_id value to HWDB table
        hw_unit = db.session.query(hwdb.HwDbModel).get(hw_unit_id)
        hw_unit.last_maintenance_id = maintenance_doc.id
        db.session.add(hw_unit)
        db.session.commit()

        # add record to MAINTENANCE_DB table
        maintenance_record = hwdb.MaintenanceDbModel(doc_id=maintenance_doc.id, hw_unit_id=hw_unit_id, status_id=1)
        db.session.add(maintenance_record)
        db.session.commit()

    except Exception as e:
        # TODO: Add logging
        print(f"Database error: {e}")

    # redirect back to hardware list
    return redirect(url_for("hwdb_list.index"))


@hwdb_maintenance.route("/maintenance_del_last", methods=['GET', ])
def maintenance_del_last():
    """
    Delete last unit maintenance info from DB
    :return: redirect back to hardware list
    """
    # get parameters form GET request
    hw_unit_id = request.args.get('hw_id', 0, type=int)
    m_id = request.args.get('m_id', 0, type=int)

    try:
        # set last_maintenance_id to zero (HW_DB table)
        hw_unit = db.session.query(hwdb.HwDbModel).get(hw_unit_id)
        hw_unit.last_maintenance_id = 0
        db.session.add(hw_unit)
        db.session.commit()

        # find maintenance record (MAINTENANCE_DB table)
        maintenance_record = db.session.query(hwdb.MaintenanceDbModel)\
            .filter(hwdb.MaintenanceDbModel.doc_id == m_id, hwdb.MaintenanceDbModel.hw_unit_id == hw_unit_id).first()

        # delete this record
        if maintenance_record is not None:
            db.session.delete(maintenance_record)
            db.session.commit()

    except Exception as e:
        # TODO: Add logging
        print(f"Database error: {e}")

    # redirect back to hardware list
    return redirect(url_for("hwdb_list.index"))


@hwdb_maintenance.route("/maintenance_report", methods=['GET', ])
def maintenance_report():
    """
    Render maintenance report table
    """
    maintenance_doc = []

    # get parameters form GET request
    maintenance_id = request.args.get('m_id', 0, type=int)

    try:
        # list of hw units with id=maintenance_id
        report_list = db.session.query(hwdb.HwDbModel)\
                        .filter(hwdb.HwDbModel.last_maintenance_id == maintenance_id)\
                        .order_by(hwdb.HwDbModel.invnum.asc(), hwdb.HwDbModel.type_id.asc())\
                        .all()

        # document requisites
        maintenance_doc = db.session.query(hwdb.MaintenanceDocsDbModel).get(maintenance_id)

    except Exception as e:
        report_list = []
        # TODO: Add logging
        print(f"Database error: {e}")

    return render_template("maintenance_report.html", report_list=report_list, doc=maintenance_doc)
