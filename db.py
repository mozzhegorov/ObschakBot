import sqlite3
from typing import List, Union

# TODO: добавить имя базы в переменную виртуального окружения
DATABASE_NAME = 'db/basketbot.db'

CREATE_DATA_TABLE = """
    CREATE TABLE IF NOT EXISTS 'cashdata' (
        id INTEGER NOT NULL PRIMARY KEY,
        user_id INTEGER NOT NULL, 
        calc_id INTEGER NOT NULL, 
        calc_alias VARCHAR(50), 
        receipt_id INTEGER NOT NULL, 
        sponsor VARCHAR(50) NOT NULL, 
        sum FLOAT NOT NULL, 
        consumer_1 VARCHAR(50), 
        consumer_2 VARCHAR(50), 
        consumer_3 VARCHAR(50), 
        consumer_4 VARCHAR(50), 
        consumer_5 VARCHAR(50), 
        consumer_6 VARCHAR(50), 
        consumer_7 VARCHAR(50), 
        consumer_8 VARCHAR(50), 
        consumer_9 VARCHAR(50), 
        consumer_10 VARCHAR(50), 
        consumer_11 VARCHAR(50), 
        consumer_12 VARCHAR(50), 
        consumer_13 VARCHAR(50), 
        consumer_14 VARCHAR(50), 
        consumer_15 VARCHAR(50), 
        consumer_16 VARCHAR(50), 
        consumer_18 VARCHAR(50), 
        consumer_19 VARCHAR(50), 
        consumer_20 VARCHAR(50) 
    );
"""
CREATE_NEW_DATA_TABLE = """
    DROP TABLE IF EXISTS 'cashdata';
    CREATE TABLE 'cashdata' (
        id INTEGER NOT NULL PRIMARY KEY,
        user_id INTEGER NOT NULL, 
        calc_id INTEGER NOT NULL, 
        calc_alias VARCHAR(50), 
        receipt_id INTEGER NOT NULL, 
        sponsor VARCHAR(50) NOT NULL, 
        sum FLOAT NOT NULL, 
        consumer_1 VARCHAR(50), 
        consumer_2 VARCHAR(50), 
        consumer_3 VARCHAR(50), 
        consumer_4 VARCHAR(50), 
        consumer_5 VARCHAR(50), 
        consumer_6 VARCHAR(50), 
        consumer_7 VARCHAR(50), 
        consumer_8 VARCHAR(50), 
        consumer_9 VARCHAR(50), 
        consumer_10 VARCHAR(50), 
        consumer_11 VARCHAR(50), 
        consumer_12 VARCHAR(50), 
        consumer_13 VARCHAR(50), 
        consumer_14 VARCHAR(50), 
        consumer_15 VARCHAR(50), 
        consumer_16 VARCHAR(50), 
        consumer_18 VARCHAR(50), 
        consumer_19 VARCHAR(50), 
        consumer_20 VARCHAR(50) 
    );
"""
CREATE_NOW_CALC_TABLE = """
    CREATE TABLE IF NOT EXISTS 'calc_now' (
        id INTEGER NOT NULL PRIMARY KEY,
        user_id INTEGER NOT NULL, 
        calc_id INTEGER NOT NULL,
        calc_alias VARCHAR(50)
    );
"""
CREATE_NEW_NOW_CALC_TABLE = """
    DROP TABLE IF EXISTS 'calc_now';
    CREATE TABLE 'calc_now' (
        id INTEGER NOT NULL PRIMARY KEY,
        user_id INTEGER NOT NULL, 
        calc_id INTEGER NOT NULL,
        calc_alias VARCHAR(50)
    );
"""
INSERT_RECEIPT = """
    INSERT INTO 'cashdata' VALUES 
    (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ;
"""
GET_LAST_CALC = """
    SELECT calc_alias, receipt_id from 'cashdata'
    WHERE user_id=? and calc_id=?
"""
GET_LAST_RECEIPT_DATA = """
SELECT cn.calc_id, cn.calc_alias, receipt_id FROM cashdata
JOIN calc_now cn on cashdata.user_id = cn.user_id and cashdata.calc_id = cn.calc_id
WHERE cn.calc_id = cashdata.calc_id and cn.user_id = ?
ORDER BY receipt_id DESC
LIMIT 1
"""
GET_ALL_RECEIPT_DATA = """
SELECT * FROM cashdata
JOIN calc_now cn on cashdata.user_id = cn.user_id and cashdata.calc_id = cn.calc_id
WHERE cn.calc_id = cashdata.calc_id and cn.user_id = ? and cn.calc_id = ?
"""
ALL_CALCS = """
SELECT calc_id, calc_alias FROM cashdata
WHERE user_id = ?
"""
LAST_CALC_DATA = """
SELECT calc_id, calc_alias FROM calc_now
WHERE user_id = ?
ORDER BY calc_id DESC
LIMIT 1
"""
INSERT_CALC = """
    INSERT INTO 'calc_now' VALUES 
    (null, ?, ?, ?) ;
"""
DELETE_CALC_FROM_CALCS = """
    DELETE FROM 'calc_now' 
    WHERE calc_id=? and user_id=?;
"""
DELETE_CALC_FROM_CASHDATA = """
    DELETE FROM 'cashdata' 
    WHERE calc_id=? and user_id=?;
"""
DELETE_ALL_CALCS_FROM_CASHDATA = """
    DELETE FROM 'cashdata' 
    WHERE user_id=?;
"""
DELETE_ALL_CALCS_FROM_CALCS = """
    DELETE FROM 'calc_now' 
    WHERE user_id=?;
"""
GET_CALC_ALIAS = """
    SELECT calc_alias FROM 'cashdata' 
    WHERE user_id=? and calc_id=?
    LIMIT 1;
"""
GET_CALC_BY_USER = """
    SELECT calc_id, calc_alias FROM 'calc_now' 
    WHERE user_id=?;
"""
GET_CALC_BY_USER_CALCID_IN_CASHS = """
    SELECT calc_alias FROM 'cashdata' 
    WHERE user_id=? and calc_id=?;
"""
GET_CALC_BY_USER_CALCID_IN_CALCS = """
    SELECT calc_alias FROM 'cashdata' 
    WHERE user_id=? and calc_id=?;
"""
ALL_CALCS = """
    SELECT * FROM 'calc_now';
"""
ALL_DATA = """
    SELECT * FROM 'cashdata';
"""
UPDATE_CALC = """
    UPDATE 'calc_now' 
    SET calc_id=?,
        calc_alias=?
    WHERE user_id=?;
"""


def create_tables():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(ALL_DATA)
        table_exists = cursor.fetchall()
        if table_exists:
            cursor.executescript(CREATE_DATA_TABLE)

        cursor.execute(ALL_CALCS)
        table_exists = cursor.fetchall()
        if table_exists:
            cursor.executescript(CREATE_NOW_CALC_TABLE)


def data_base_action(script, inserted_data=None):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        if inserted_data:
            cursor.execute(script, inserted_data)
        else:
            cursor.executescript(script)


def data_base_fetch(script, inserted_data=None):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        return cursor.execute(script, inserted_data).fetchall()


def data_base_fetchone(script, inserted_data=None):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        return cursor.execute(script, inserted_data).fetchone()


if __name__ == '__main__':
    create_tables()
