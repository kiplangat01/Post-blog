import os


class Config:
    

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.environ.get('SECRET_KEY')

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'apollolibrary99@gmail.com'
    MAIL_PASSWORD =  os.environ.get('MAIL_PASSWORD')

    MAIL_USE_TLS = False
    MAIL_USE_SSL = True


class ProdConfig(Config):
   ...


class DevConfig(Config):
   
    DEBUG = True


config_options = {
    'dev': DevConfig,
    'product': ProdConfig
}
