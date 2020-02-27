# from app.main import db
from main import db

"""
`id` INT(10) NOT NULL AUTO_INCREMENT,
`invnum` VARCHAR(12) NOT NULL DEFAULT '',
`type_id` INT(10) UNSIGNED NOT NULL,
`legacy_user` VARCHAR(50) NULL DEFAULT '\'NA\'',
`empl_id` INT(11) NOT NULL DEFAULT '0',
`location` VARCHAR(4) NOT NULL,
`status_id` INT(10) NOT NULL,
`manuf` VARCHAR(20) NOT NULL DEFAULT '\'NA\'',
`model` VARCHAR(64) NOT NULL DEFAULT '\'NA\'',
`vendor_id` INT(10) UNSIGNED NULL DEFAULT '0',
`serialnum` VARCHAR(64) NOT NULL DEFAULT '\'NA\'',
`year` YEAR NOT NULL DEFAULT '1999',
`warranty` INT(2) NOT NULL DEFAULT '12',
`accounting` DATE NULL DEFAULT '1999-01-21',
`comments` TEXT NULL,
`buhtext` VARCHAR(80) NULL DEFAULT NULL,
`buh_os` INT(1) NOT NULL DEFAULT '1',
`check` INT(1) NOT NULL DEFAULT '0',
`gas_id` INT(1) NOT NULL DEFAULT '0',
`last_maintenance_id` INT(1) NOT NULL DEFAULT '0',
`lastupdated` TIMESTAMP NULL DEFAULT NULL,
"""


class HwDbModel(db.Model):
    """
    Model class for HW_DB table
    """

    __tablename__ = "hw_db"

    id = db.Column(db.Integer, primary_key=True)
    invnum = db.Column(db.String(12))
    type_id = db.Column(db.Integer, db.ForeignKey("hw_types.id"))
    hw_type = db.relationship("HwTypesModel", backref="hw_db", lazy="joined")
    legacy_user = db.Column(db.String(50))
    empl_id = db.Column(db.Integer, db.ForeignKey("empl_list_gas.id"))
    empl_fio = db.relationship("EmplListGasModel", backref="hw_db", lazy="joined")
    location = db.Column(db.String(4))
    status_id = db.Column(db.Integer, db.ForeignKey("hw_statuses.id"))
    status = db.relationship("HwStatusesModel", backref="hw_db", lazy="joined")
    manuf = db.Column(db.String(20))
    model = db.Column(db.String(64))
    vendor_id = db.Column(db.Integer)
    serialnum = db.Column(db.String(64))
    year = db.Column(db.Integer)
    warranty = db.Column(db.Integer)
    accounting = db.Column(db.DateTime)
    comments = db.Column(db.Text)
    buhtext = db.Column(db.String(80))
    buh_os = db.Column(db.Integer)
    check = db.Column(db.Integer)
    gas_id = db.Column(db.Integer)
    last_maintenance_id = db.Column(db.Integer, db.ForeignKey("maintenance_docs_db.id"))
    last_maintenance = db.relationship("MaintenanceDocsDbModel", backref="hw_db", lazy="joined")

    def __init__(self, invnum, type_id, legacy_user, empl_id, location,
                 status_id, manuf, model, vendor_id, serialnum, year, warranty,
                 accounting, comments, buhtext, buh_os, check, gas_id,
                 last_maintenance_id):
        self.invnum = invnum
        self.type_id = type_id
        self.legacy_user = legacy_user
        self.empl_id = empl_id
        self.location = location
        self.status_id = status_id
        self.manuf = manuf
        self.model = model
        self.vendor_id = vendor_id
        self.serialnum = serialnum
        self.year = year
        self.warranty = warranty
        self.accounting = accounting
        self.comments = comments
        self.buhtext = buhtext
        self.buh_os = buh_os
        self.check = check
        self.gas_id = gas_id
        self.last_maintenance_id = last_maintenance_id

    def __repr__(self):
        return f"{self.invnum} - {self.manuf} {self.model}"


"""
    `id` INT(10) NOT NULL DEFAULT '0',
    'hw_type` VARCHAR(64) NOT NULL,
    `hw_type_ru` VARCHAR(64) NOT NULL
"""


class HwTypesModel(db.Model):
    """
        Model class for HW_TYPES table
    """

    __tablename__ = "hw_types"

    id = db.Column(db.Integer, primary_key=True)
    hw_type = db.Column(db.String(64))
    hw_type_ru = db.Column(db.String(64))

    def __init__(self, hw_type, hw_type_ru):
        self.hw_type = hw_type
        self.hw_type_ru = hw_type_ru

    def __repr__(self):
        return f"{self.hw_type_ru}"


"""
    `status_id` INT(10) NOT NULL DEFAULT '0',
    `status_name` VARCHAR(64) NULL DEFAULT NULL,
    `status_name_ru` VARCHAR(64) NULL DEFAULT NULL
"""


class HwStatusesModel(db.Model):

    __tablename__ = "hw_statuses"

    id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(64))
    status_name_ru = db.Column(db.String(64))

    def __init__(self, status_name, status_name_ru):
        self.status_name = status_name
        self.status_name_ru = status_name_ru

    def __repr__(self):
        return f"{self.status_name_ru}"


"""
    `id` INT(10) NOT NULL AUTO_INCREMENT,
    `fio` VARCHAR(128) NOT NULL DEFAULT '0',
    `tab_no` VARCHAR(128) NOT NULL DEFAULT '0',
    `depts` VARCHAR(256) NOT NULL DEFAULT '0',
    `post` VARCHAR(256) NOT NULL DEFAULT '0',
    `post_dop` VARCHAR(256) NOT NULL DEFAULT '0',
    `date_recr` VARCHAR(16) NOT NULL DEFAULT '0',
    `date_post` VARCHAR(16) NOT NULL DEFAULT '0',
    `sx` VARCHAR(16) NOT NULL DEFAULT '0',
    `date_birth` VARCHAR(16) NOT NULL DEFAULT '0',
"""


class EmplListGasModel(db.Model):
    """
        Model class for EMPL_LIST_GAS table
    """

    __tablename__ = "empl_list_gas"

    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(128))
    tab_no = db.Column(db.String(128))
    depts = db.Column(db.String(256))
    post = db.Column(db.String(256))
    post_dop = db.Column(db.String(256))
    date_recr = db.Column(db.DateTime)
    date_post = db.Column(db.DateTime)
    sx = db.Column(db.String(16))
    date_birth = db.Column(db.DateTime)

    def __init__(self, fio, tab_no, depts, post, post_dop, date_recr, date_post, sx, date_birth):
        self.fio = fio
        self.tab_no = tab_no
        self.depts = depts
        self.post = post
        self.post_dop = post_dop
        self.date_recr = date_recr
        self.date_post = date_post
        self.sx = sx
        self.date_birth = date_birth

    def __repr__(self):
        return f"{self.fio}"


"""
    `id` INT(10) NOT NULL AUTO_INCREMENT,
    `year` INT(11) NOT NULL DEFAULT '1999',
    `doc_date` DATE NULL DEFAULT '1999-01-21',
    `doc_num` VARCHAR(16) NOT NULL DEFAULT '',
    `units_qty` INT(11) NOT NULL DEFAULT '0',
    `units_id_list` VARCHAR(2048) NOT NULL DEFAULT '',
    `lastupdated` TIMESTAMP NULL DEFAULT NULL,
"""


class MaintenanceDocsDbModel(db.Model):

    __tablename__ = "maintenance_docs_db"

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    doc_date = db.Column(db.DateTime)
    doc_num = db.Column(db.String(16))
    units_qty = db.Column(db.Integer)
    units_id_list = db.Column(db.String(2048))

    def __init__(self, year, doc_date, doc_num, units_qty, units_id_list):
        self.year = year
        self.doc_date = doc_date
        self.doc_num = doc_num
        self.units_qty = units_qty
        self.units_id_list = units_id_list

    def __repr__(self):
        return f"№{self.doc_num} от {self.doc_date}"


"""
`id` INT(10) NOT NULL AUTO_INCREMENT,
`doc_id` INT(10) NOT NULL,
`hw_unit_id` INT(10) NOT NULL,
`status_id` INT(10) NOT NULL,
"""


class MaintenanceDbModel(db.Model):

    __tablename__ = "maintenance_db"

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer)
    hw_unit_id = db.Column(db.Integer)
    status_id = db.Column(db.Integer)

    def __init__(self, doc_id, hw_unit_id, status_id):
        self.doc_id = doc_id
        self.hw_unit_id = hw_unit_id
        self.status_id = status_id

    def __repr__(self):
        # return f"{self.doc_id} {self.hw_unit_id}"
        return f"doc:{self.doc_id} hw:{self.hw_unit_id}"
