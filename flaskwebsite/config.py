import os


class Config:
    FLASK_APP = 'flaskwebsite'
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/databasename'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = 'your_password_salt'
    MAIL_SERVER = 'your_mail_server'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'your_email'
    MAIL_PASSWORD = 'your_email_password'

