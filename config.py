import os
import logging


class Config(object):
    APP_VERSION = '191100000'
    CONFIG_NAME = 'base'
    # BASE_URL = ''
    HOST = '0.0.0.0'
    PORT = 8000
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    APP_DIR = BASE_DIR + '/app'
    STATIC_URL_PATH = '/assets'
    STATIC_FOLDER = APP_DIR + '/assets'
    TEMPLATE_FOLDER = APP_DIR + '/templates'
    TEMPLATES_AUTO_RELOAD = True
    
    UPLOADED_PATH = os.path.join(BASE_DIR, 'uploads')
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_HEIGHT = 400
    CKEDITOR_FILE_UPLOADER = 'base.upload'

    SECRET_KEY = 'rMxFGtrOkF1@m5fEU#5x2A32Ygxu8P6x5ATr^PwA'

    #
    TESTING = False
    DEBUG = False
    LOGGER_LEVEL = logging.NOTSET

    # rds:postgresql
    pg_db_username = 'Bora'
    pg_db_password = ''
    pg_db_name = 'endless_end'
    pg_db_hostname = 'localhost'
    SQLALCHEMY_DATABASE_URI = 'postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}'.format(DB_USER=pg_db_username, DB_PASS=pg_db_password, DB_ADDR=pg_db_hostname, DB_NAME=pg_db_name)
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # aws
    AWS_SES_ACCESS_KEY_ID = ''
    AWS_SES_SECRET_ACCESS_KEY = ''
    AWS_SES_REGION_NAME = ''
    AWS_SES_FROM_EMAIL = ''
    AWS_SES_FROM_NAME = ''

    NOTIFY_EMAILS_TO_ADMIN = None
    NOTIFY_EMAILS_TO_DEVELOPER = None

class ProductionConfig(Config):
    CONFIG_NAME = 'production'
    DEBUG = False
    LOGGER_LEVEL = logging.WARNING


class TestingConfig(Config):
    CONFIG_NAME = 'testing'
    DEBUG = False
    LOGGER_LEVEL = logging.NOTSET


class DevelopmentConfig(Config):
    CONFIG_NAME = 'development'
    DEBUG = True
    LOGGER_LEVEL = logging.NOTSET


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
