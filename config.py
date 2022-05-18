import os
from flask_bcrypt import Bcrypt

class Config:
    

    SQLALCHEMY_DATABASE_URI = 'postgresql://moringa:bca321@localhost:5432/post'

    SECRET_KEY = 'code for better'

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
