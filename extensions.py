from flask_restful import Api
import MySQLdb
from config import config


def request_db_connection():
    return MySQLdb.connect(host=config.MYSQL_HOST, user=config.MYSQL_USER, passwd=config.MYSQL_PASSWORD,
                           db=config.MYSQL_DB, autocommit=True)


api = Api()
