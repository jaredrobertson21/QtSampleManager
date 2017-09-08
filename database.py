import sqlite3
import time
import datetime


# adds sample information to the database
def addSampleToDatabase(db, cursor, name, chemical, notes):
    unix = int(time.time())
    datestamp = str(datetime.datetime.fromtimestamp(unix).strftime("%Y-%m-%d %H:%M:%S"))
    cursor.execute('INSERT INTO sample_table(datestamp, sample_name, chemical_name, sample_notes) \
                    VALUES (?, ?, ?, ?)', (datestamp, name, chemical, notes))
    db.commit()


# upon project initialization, creates the table where sample data is stored
def createTable(cursor):
    cursor.execute('CREATE TABLE IF NOT EXISTS sample_table(datestamp text, sample_name text, \
                    chemical_name text, sample_notes text)')


# deletes the selected samples from the database
# sample is passed as a SampleLibrary object
# TODO: incomplete
def deleteSample(cursor, sample):
    cursor.execute('DELETE FROM sample_table \
                    WHERE ')


# returns all sample data from the database
def getAllData(cursor):
    cursor.execute('SELECT sample_name, chemical_name, sample_notes \
                    FROM sample_table')
    data = cursor.fetchall()
    return data