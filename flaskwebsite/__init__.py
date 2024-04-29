from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth
from flaskwebsite.config import Config
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
oauth = OAuth()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app, supports_credentials=True)
    app.secret_key = config_class.SECRET_KEY
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.session_protection = "strong"
    mail.init_app(app)
    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id='your_google_client_id',
        client_secret='your_google_client_secret',
        access_token_url='https://accounts.google.com/o/oauth2/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        client_kwargs={'scope': 'openid profile email'},
    )

    from flaskwebsite.user.routes import user
    from flaskwebsite.main.routes import main

    app.register_blueprint(user)
    app.register_blueprint(main)

    return app