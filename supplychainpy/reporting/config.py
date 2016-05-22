import os


class Config(object):
    pass


class ProdConfig(Config):
    pass


class DevConfig(Config):
    PWD = os.path.abspath(os.curdir)
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/reporting.db'.format(PWD)
    SECRET_KEY = '|~G\xde\xa7\x9b\x1aKaZ-\xabk8\x0b\x12\xee)\xe0\xe0\x8b\x0c\xd9\x1d'
    SESSION_PROTECTION = 'strong'
    SQLALCHEMY_ECHO = True

