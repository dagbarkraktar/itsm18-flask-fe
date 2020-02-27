from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
import json


# from app.models import hwdb
from models import hwdb
# from app.main import db
from main import db

import logging
import log.log_config

hwdb_list = Blueprint("hwdb_list", __name__)

# default sort conditions
sort_conditions_default = {"location": "asc", "manuf": "none", "model": "none", "year": "none"}
# default filters dict (show all records)
hw_filters_default = {}

# retrieve logger
srv_logger = logging.getLogger("srv_log")

@hwdb_list.route("/", methods=["GET", "POST"])
def index():
    """
    Endpoint for rendering hardware list page
    :return:
    """

    # Set sort conditions (from session or default)
    if "sort_conditions" in session:
        sort_conditions = session.get("sort_conditions")
        # TODO: add sort_conditions dictionary checking
    else:
        sort_conditions = sort_conditions_default
        session["sort_conditions"] = sort_conditions_default

    # print(f"INDEX: sort_conditions: {sort_conditions}")

    # build sort condition list
    conditions_list = []
    for field_name, field_cond in sort_conditions.items():
        # print(f"{field_name}:{field_cond}")
        if field_cond != "none":
            field = getattr(hwdb.HwDbModel, field_name)
            if field_cond == "asc":
                conditions_list.append(field.asc())
            if field_cond == "desc":
                conditions_list.append(field.desc())

    # print(f"INDEX: Condition list: {len(conditions_list)} elements")

    # Set filters list (from session or default)
    if "hw_filters" in session:
        hw_filters = session.get("hw_filters")
    else:
        hw_filters = hw_filters_default
        session["hw_filters"] = hw_filters_default

    # Get hardware list via SQLAlchemy
    try:
        # Apply sort conditions (invnum is always sort by ascending)
        hw_query = db.session.query(hwdb.HwDbModel).order_by(*conditions_list, hwdb.HwDbModel.invnum.asc())

        # Apply filters
        for field_name, value in hw_filters.items():
            field = getattr(hwdb.HwDbModel, field_name)
            hw_query = hw_query.filter(field == value)
            # print(f"APPLY FILTER: {field_name}={value}")

        # Don't show write_off units (status_id=7)
        hw_query = hw_query.filter(hwdb.HwDbModel.status_id != 7)
        # print(f"APPLY FILTER: status_id!=7")

        # run query
        hw_list = hw_query.all()

        srv_logger.info(f"Index query OK!")

    except Exception as e:
        # TODO: Add logging
        print(f"Database error: {e}")
        srv_logger.error(f"Database error: {e}")
        hw_list = []

    # render page with retrieved hw list
    return render_template("index.html", hw_list=hw_list, hw_filters=hw_filters, sort_conditions=sort_conditions)


def rotate_sort_condition(condition):
    """
    Helper function for rotate values of sort condition: asc -> desc -> none
    :param condition: current sort condition
    :return: next sort condition
    """
    if condition == "asc":
        return "desc"
    elif condition == "desc":
        return "none"
    elif condition == "none":
        return "asc"



@hwdb_list.route("/hw_sort", methods=["GET"])
def hw_sort():
    """
    Endpoint for managing sort conditions.
    :return: Set conditions and redirect to /index
    """

    # get args (form GET request)
    args_dict = request.args.to_dict()
    # print(f"HW_SORT: GET args: {args_dict}")

    # set default sort conditions
    if "sort_conditions" not in session:
        session["sort_conditions"] = sort_conditions_default
        print("HW_SORT: Set default conditions.")

    field_name = args_dict["field"]
    condition = session["sort_conditions"][field_name]
    session["sort_conditions"][field_name] = rotate_sort_condition(condition)
    session.modified = True

    # print(f"HW_SORT: sort_conditions: {session['sort_conditions']}")

    return redirect(url_for("hwdb_list.index"))


@hwdb_list.route("/hw_filter")
def hw_filter():
    """
    Endpoint for managing filters
    :return:
    """

    # get args (form GET request)
    args_dict = request.args.to_dict()
    print(f"HW_FILTER: GET args: {args_dict}")

    # Set filters
    if "hw_filters" not in session:
        session["hw_filters"] = hw_filters_default

    # TODO: check args exists
    # TODO: check field
    field_name = args_dict["field"]
    field_value = args_dict["value"]
    action = args_dict["action"]

    if action == "del":
        del session["hw_filters"][field_name]
        session.modified = True

    if action == "add":
        session["hw_filters"][field_name] = field_value
        session.modified = True

    return redirect(url_for("hwdb_list.index"))


@hwdb_list.route("/hwunits/<int:hw_unit_id>")
def hwunits(hw_unit_id):
    """

    :param hw_unit_id:
    :return:
    """
    hw_unit_dict = {}
    hw_unit = db.session.query(hwdb.HwDbModel).get(hw_unit_id)

    hw_unit_dict["invnum"] = hw_unit.invnum
    hw_unit_dict["hw_type"] = str(hw_unit.hw_type)
    hw_unit_dict["manuf"] = hw_unit.manuf
    hw_unit_dict["model"] = hw_unit.model
    hw_unit_dict["serialnum"] = hw_unit.serialnum
    hw_unit_dict["year"] = hw_unit.year

    return json.dumps(hw_unit_dict)


@hwdb_list.route("/hw_unit_edit_form", methods=['GET', 'POST'])
def hw_unit_edit_form():
    """
    Endpoint for rendering hw_unit_edit_form
    :return:
    """
    # get record_id (form GET request)
    hw_unit_id = request.args.get('hw_id', 0, type=int)

    # SELECT ... WHERE ID=HW_UNIT_ID
    hw_unit = db.session.query(hwdb.HwDbModel).get(hw_unit_id)

    # Get list of hardware types
    hw_types = db.session.query(hwdb.HwTypesModel).all()
    # Get list of users
    employees = db.session.query(hwdb.EmplListGasModel).all()
    # Get list of statuses
    hw_statuses = db.session.query(hwdb.HwStatusesModel).all()

    # check hw_unit exist
    if hw_unit is None:
        return redirect(url_for("hwdb_list.index"))
    else:
        # render page with edit form
        return render_template("hw_form_edit.html", hw_unit=hw_unit, hw_types_dict=hw_types, empl_dict=employees,
                               hw_statuses=hw_statuses)


@hwdb_list.route("/hw_unit_update", methods=['POST', ])
def hw_unit_update():
    """
    Endpoint: Get data from form and save it to DB
    :return:
    """
    if request.method == "POST":
        form_data = request.form.to_dict()

        # TODO: Add form fields validation
        hw_id = form_data['hw_id']
        hw_type_id = form_data['hw_type_id']
        hw_status_id = form_data['hw_status_id']
        hw_location = form_data['hw_location']
        hw_empl_id = form_data['hw_empl_id']
        hw_manuf = form_data['hw_manuf']
        hw_model = form_data['hw_model']
        hw_serialnum = form_data['hw_serialnum']
        hw_year = form_data['hw_year']
        hw_warranty = form_data['hw_warranty']
        hw_accounting = form_data['hw_accounting']

        hw_unit = db.session.query(hwdb.HwDbModel).get(hw_id)

        hw_unit.type_id = hw_type_id
        hw_unit.status_id = hw_status_id
        hw_unit.location = hw_location
        hw_unit.empl_id = hw_empl_id
        hw_unit.manuf = hw_manuf
        hw_unit.model = hw_model
        hw_unit.serialnum = hw_serialnum
        hw_unit.year = hw_year
        hw_unit.warranty = hw_warranty
        hw_unit.accounting = hw_accounting

        db.session.add(hw_unit)
        db.session.commit()

        print(f"HW_UNIT: {hw_unit} saved into DB.")

    return redirect(url_for("hwdb_list.index"))