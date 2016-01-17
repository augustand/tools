# -*- coding: utf-8 -*-

import MySQLdb as mdb
import logging
from python.logger import logger

__author__ = 'haining'
logger.setLevel(logging.DEBUG)

db = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "passwd": "",
    "db": "database"
}


class MSDB():
    # TODO thread pool
    def __init__(self, database):
        if not isinstance(database, dict):
            raise TypeError("MSDB(db), db must be dict")
        self.__db = database

    def get_connect(self):
        # 建议指定时区
        con = mdb.connect(host=self.__db["host"], port=self.__db["port"], user=self.__db["user"], passwd=self.__db["passwd"], db=self.__db["db"], charset="utf8")
        return con

DB = MSDB(db)


def fetch_sql(sql=None, res=False, *args):  # 这个方法写的真是难用
    """  这个方法感觉真的很难用
    :param res: 返回结果形态, True 返回内容,False 返回受影响行
    :param sql:
    :param args:
    :return:
    """
    if not sql:
        logger.error("sql is nil")
        return []

    try:
        con = DB.get_connect()
        cur = con.cursor()
        sql_log = sql % args
        row = cur.execute(sql, args)  # 预编译防止sql 注入
        con.commit()
        logger.info('sql: '+sql_log)
        con.close()
        if not res:
            # cur.lastrowid
            return row
        else:
            return list(cur.fetchall())
    except Exception, e:
        sql_log = sql % args
        logger.error('sql: '+sql_log+', error: '+str(e))
        return []


def return_dict(key, value):
    """
    two list to dict
    :param key:
    :param value:
    :return: list(dict, dict)
    """
    try:
        if len(key) == len(value) and False in [isinstance(i, tuple) for i in value] and False in [isinstance(i, list) for i in value]:
            return dict(zip(key, value))
        else:
            return [dict(zip(key, r)) for r in value]
    except Exception, e:
        logger.error("error,"+str(e)+" Dao input key value is not equal, please check Dao : "+str(key)+str(value))
        return {}

if __name__ == "__main__":
    logger.info(return_dict(["name", "age"], [["whnzy", 16], ["haining", 22]]))
    logger.info(return_dict(["brand_name", "id"], [("whnzy", 16), ("haining", 22)]))