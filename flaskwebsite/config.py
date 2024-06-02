import os


class Config:
    FLASK_APP = 'flaskwebsite'
    SECRET_KEY = '5XqCiHJlxk2pNUIO2Zz46NPnFAGqbNXi'
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:helloiamadmin@localhost:8085/nokia_ocr'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = 'your_password_salt'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'your_email'
    MAIL_PASSWORD = 'your_email_password'

