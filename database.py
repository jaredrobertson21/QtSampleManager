import sqlite3
import time
import datetime


def addSampleToDatabase(db, cursor, name, chemical, notes):
    unix = int(time.time())
    datestamp = str(datetime.datetime.fromtimestamp(unix).strftime("%Y-%m-%d %H:%M:%S"))
    cursor.execute('INSERT INTO sample_table(datestamp, sample_name, chemical_name, sample_notes) \
                    VALUES (?, ?, ?, ?)', (datestamp, name, chemical, notes))
    db.commit()


def createTable(cursor):
    cursor.execute('CREATE TABLE IF NOT EXISTS sample_table(datestamp text, sample_name text, \
                    chemical_name text, sample_notes text)')