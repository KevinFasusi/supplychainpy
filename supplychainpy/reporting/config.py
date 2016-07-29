import os


class Config(object):
    pass


class ProdConfig(Config):
    pass


class DevConfig(Config):
    PWD = os.path.abspath(os.curdir)
    DEBUG = False
    if os.name in ['posix', 'mac']:
        SQLALCHEMY_DATABASE_URI ='sqlite:///{}/reporting.db'.format(PWD)

    elif os.name == 'nt':
        SQLALCHEMY_DATABASE_URI = 'sqlite:///{}\\reporting.db'.format(PWD)

    SECRET_KEY = '|~G\xde\xa7\x9b\x1aKaZ-\xabk8\x0b\x12\xee)\xe0\xe0\x8b\x0c\xd9\x1d'
    SESSION_PROTECTION = 'strong'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
