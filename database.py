import sqlite3
import datetime


def create_table(cursor):
    cursor.execute('CREATE TABLE IF NOT EXISTS sample_table(datestamp text, sample_name text, \
                    chemical_name text, sample_notes text)')
    print('create_table executed')