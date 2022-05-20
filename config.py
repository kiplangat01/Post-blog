import os
from flask_bcrypt import Bcrypt

class Config:
    

    
    SECRET_KEY = 'code for better'


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://chkinbaplmeqbi:6ea240a5f211d74c1c14bc701416032a7ceee506b0295f4d6d1cf0ffda04f04b@ec2-54-204-56-171.compute-1.amazonaws.com:5432/db766ukgho86s'


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://moringa:bca321@localhost:5432/isert'

   
    DEBUG = True


config_options = {
    'dev': DevConfig,
    'prod': ProdConfig
}
