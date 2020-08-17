from constants import *
from PySide2.QtCore import Qt, QMetaObject
from PySide2.QtSql import QSql, QSqlDatabase, QSqlQuery
from PySide2.QtWidgets import QMessageBox
from DB.bulk_db import loadDbFromSQL


def get_dbfilename(app_path):
    return app_path + DB_PATH

def init_and_check_db(parent, db_path):
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(get_dbfilename(db_path))
    db.open()
    tables = db.tables(QSql.Tables)
    if not tables:
        db.close()
        loadDbFromSQL(get_dbfilename(db_path), db_path + INIT_SCRIPT_PATH)
        QMessageBox().information(parent, parent.tr("Database initialized"),
                                  parent.tr("Database have been initialized.\n"
                                          "You need to restart the application.\n"
                                          "Application terminates now."),
                                  QMessageBox.Ok)
        _ = QMetaObject.invokeMethod(parent, "close", Qt.QueuedConnection)
        return None

    query = QSqlQuery(db)
    query.exec_("SELECT value FROM settings WHERE name='SchemaVersion'")
    query.next()
    if query.value(0) != TARGET_SCHEMA:
        db.close()
        QMessageBox().critical(parent, parent.tr("Database version mismatch"),
                               parent.tr("Database schema version is wrong"),
                               QMessageBox.Ok)
        _ = QMetaObject.invokeMethod(parent, "close", Qt.QueuedConnection)
        return None
    return db


def get_base_currency(db):
    query = QSqlQuery(db)
    query.exec_("SELECT value FROM settings WHERE name='BaseCurrency'")
    query.next()
    return query.value(0)

def get_base_currency_name(db):
    query = QSqlQuery(db)
    query.exec_("SELECT name FROM assets WHERE id = (SELECT value FROM settings WHERE name='BaseCurrency')")
    query.next()
    return query.value(0)