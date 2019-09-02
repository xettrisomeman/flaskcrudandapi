

class BaseConfig:

    TESTING = True
    DEBUG = True
    SECRET_KEY = 'youcannotguessthissecretkeyboi'


class DevelopmentConfig(BaseConfig):

    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

     