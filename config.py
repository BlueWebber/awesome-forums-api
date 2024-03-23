from dotenv import load_dotenv
from os import environ
from utils.serializer import DatetimeEncoder


class Config:
    load_dotenv()
    RESTFUL_JSON = {'cls': DatetimeEncoder}
    MYSQL_HOST = environ.get('db_host')
    MYSQL_USER = environ.get('db_username')
    MYSQL_PASSWORD = environ.get('db_pass')
    MYSQL_port = environ.get('db_port')
    MYSQL_DB = environ.get('db_name')
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
    IMAGE_FORMAT = 'JPEG'
    PFP_IMAGE_FORMAT = 'PNG'
    ANIMATED_IMAGE_FORMAT = 'GIF'
    ALLOWED_IMAGE_FORMATS = {"png", "jpeg", "jpg", "gif", "bmp", "dib", "eps", "ico", "im", "ics", "msp", "pcx"}
    ALLOWED_VIDEO_FORMATS = {"mp4", "webm"}
    ALLOWED_USER_SETTINGS = {"theme"}
    PFP_SIZE = (128, 128)
    MAX_LENS_MAP = {
        "username": 45,
        "password": 1000,
        "email": 355,
        "title": 150,
        "body": 15000,
    }
    MAX_IMAGE_SIZE = 10485760
    MAX_VID_SIZE = 26214400
    ALLOWED_POST_SORT_CLAUSES = {"newest", "most_replies", "oldest"}


config = Config()
