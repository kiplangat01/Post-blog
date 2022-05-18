from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_script._compat import text_type
from flask_login import LoginManager
from flask_mail import Mail
from config import config_options
from flask_migrate import Migrate
bootstrap = Bootstrap()
migrate = Migrate()

db = SQLAlchemy()
mail=Mail()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'

login_manager.login_message_category = 'infomation'


def create_app(config_name):

    app = Flask(__name__)

    app.config.from_object(config_options[config_name])
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app,db)
    
    bcrypt.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    from app.main.views import users
    # from app.views import posts
    from app.main.views import main

    app.register_blueprint(main)
    app.register_blueprint(users)
    # app.register_blueprint(posts)

    return app

