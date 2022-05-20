import os
from flask_bcrypt import Bcrypt

class Config:
    

    SQLALCHEMY_DATABASE_URI = 'postgresql://moringa:bca321@localhost:5432/isert'

    SECRET_KEY = 'code for better'


class ProdConfig(Config):
   ...


class DevConfig(Config):
   
    DEBUG = True


config_options = {
    'dev': DevConfig,
    'product': ProdConfig
}
