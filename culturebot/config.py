import os
basedir = os.path.abspath(os.path.dirname(__file__))
databasedir = os.environ.get('DATABASE_PATH') or \
              os.path.join(basedir, "db")


class Config(object):
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'secret-key-to-come'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(databasedir, 'culturebot.db')


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    TESTING = True