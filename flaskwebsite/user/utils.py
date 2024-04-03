import hashlib
from flask import current_app, url_for
from models import User
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from flaskwebsite import mail


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def validate_username(username):
    user = User.query.filter_by(username=username.data).first()
    return bool(user)


def validate_email(email):
    user = User.query.filter_by(email=email.data).first()
    return bool(user)


def send_verification_email(user_email, username):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = serializer.dumps(user_email, salt=current_app.config['SECURITY_PASSWORD_SALT'])
    verify_url = url_for('verify_email', token=token, _external=True)
    msg = Message('Confirm your email', sender=current_app.config['MAIL_USERNAME'], recipients=[user_email])
    msg.body = f'Hi {username}, please click on the link to verify your email address: {verify_url}'
    mail.send(msg)
