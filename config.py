from dotenv import load_dotenv
from os import environ
load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{environ.get('db_username')}:{environ.get('db_pass')}@" \
                              f"{environ.get('db_host')}/{environ.get('db_name')}"
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    NUMBER_OF_POST_PAGES = 20
    ALLOWED_ORIGINS = '*'
    ALLOWED_METHODS = "GET, POST, OPTIONS, PUT, DELETE"
    ALLOWED_HEADERS = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With, x-auth-token"
    EXPOSED_HEADERS = "x-auth-token"
    EXPIRY_TIME_MINS = 0
    EXPIRY_TIME_HOURS = 72
    AUTH_TOKEN_NAME = 'x-auth-token'


config = Config()
