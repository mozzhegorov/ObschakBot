import psycopg2 as dbdriver

from typing import List, Union
import environ

env = environ.Env()
environ.Env.read_env()


# TODO: добавить имя базы в переменную виртуального окружения
# DATABASE_NAME = 'basketbot.db'
DATABASE_NAME = env.get_value('DATABASE_URL')

CREATE_DATA_TABLE = """
    CREATE TABLE IF NOT EXISTS cashdata (
        id SERIAL PRIMARY KEY,
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
    DROP TABLE IF EXISTS cashdata;
    CREATE TABLE cashdata (
        id SERIAL PRIMARY KEY,
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
    CREATE TABLE IF NOT EXISTS calc_now (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL, 
        calc_id INTEGER NOT NULL,
        calc_alias VARCHAR(50)
    );
"""
CREATE_NEW_NOW_CALC_TABLE = """
    DROP TABLE IF EXISTS calc_now;
    CREATE TABLE calc_now (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL, 
        calc_id INTEGER NOT NULL,
        calc_alias VARCHAR(50)
    );
"""
INSERT_RECEIPT = """
    INSERT INTO cashdata VALUES 
    (default, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ;
"""
GET_LAST_CALC = """
    SELECT calc_alias, receipt_id from cashdata
    WHERE user_id=%s and calc_id=%s
"""
GET_LAST_RECEIPT_DATA = """
SELECT cn.calc_id, cn.calc_alias, receipt_id FROM cashdata
JOIN calc_now cn on cashdata.user_id = cn.user_id and cashdata.calc_id = cn.calc_id
WHERE cn.calc_id = cashdata.calc_id and cn.user_id = %s
ORDER BY receipt_id DESC
LIMIT 1
"""
GET_ALL_RECEIPT_DATA = """
SELECT * FROM cashdata
JOIN calc_now cn on cashdata.user_id = cn.user_id and cashdata.calc_id = cn.calc_id
WHERE cn.calc_id = cashdata.calc_id and cn.user_id = %s and cn.calc_id = %s
"""
ALL_CALCS_BY_USER = """
SELECT calc_id, calc_alias FROM cashdata
WHERE user_id=%s
"""
LAST_CALC_DATA = """
SELECT calc_id, calc_alias FROM calc_now
WHERE user_id=%s;
"""
INSERT_CALC = """
    INSERT INTO calc_now VALUES 
    (default, %s, %s, %s) ;
"""
DELETE_CALC_FROM_CALCS = """
    DELETE FROM calc_now 
    WHERE calc_id=%s and user_id=%s;
"""
DELETE_CALC_FROM_CASHDATA = """
    DELETE FROM cashdata 
    WHERE calc_id=%s and user_id=%s;
"""
DELETE_ALL_CALCS_FROM_CASHDATA = """
    DELETE FROM cashdata 
    WHERE user_id=%s;
"""
DELETE_ALL_CALCS_FROM_CALCS = """
    DELETE FROM calc_now 
    WHERE user_id=%s;
"""
GET_CALC_ALIAS = """
    SELECT calc_alias FROM cashdata 
    WHERE user_id=%s and calc_id=%s
    LIMIT 1;
"""
GET_CALC_BY_USER = """
    SELECT calc_id, calc_alias FROM calc_now 
    WHERE user_id=%s;
"""
GET_CALC_BY_USER_CALCID_IN_CASHS = """
    SELECT calc_alias FROM cashdata 
    WHERE user_id=%s and calc_id=%s;
"""
GET_CALC_BY_USER_CALCID_IN_CALCS = """
    SELECT calc_alias FROM cashdata 
    WHERE user_id=%s and calc_id=%s;
"""
ALL_CALCS = """
    SELECT * FROM calc_now;
"""
ALL_DATA = """
    SELECT * FROM cashdata;
"""
CALCS_EXISTS = """
    SELECT * FROM information_schema.tables  
    WHERE table_name='calc_now';
"""
DATA_EXISTS = """
    SELECT * FROM information_schema.tables 
    WHERE table_name='cashdata';
"""
UPDATE_CALC = """
    UPDATE calc_now 
    SET calc_id=%s,
        calc_alias=%s
    WHERE user_id=%s;
"""


def create_tables():
    with dbdriver.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(DATA_EXISTS)
        table_exists = bool(cursor.fetchall())
        if not table_exists:
            cursor.execute(CREATE_DATA_TABLE)

        cursor.execute(CALCS_EXISTS)
        table_exists = bool(cursor.fetchall())
        if not table_exists:
            cursor.execute(CREATE_NOW_CALC_TABLE)


def data_base_action(script, inserted_data=None):
    with dbdriver.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        if inserted_data:
            cursor.execute(script, inserted_data)
        else:
            cursor.execute(script)


def data_base_fetch(script, inserted_data=None):
    with dbdriver.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(script, inserted_data)
        return cursor.fetchall()


def data_base_fetchone(script, inserted_data=None):
    with dbdriver.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(script, inserted_data)
        cursor.fetchone()


if __name__ == '__main__':
    create_tables()
