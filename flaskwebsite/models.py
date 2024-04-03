from datetime import datetime
from flask_login import UserMixin
from flaskwebsite import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    data = db.relationship('Data', backref='user', lazy=True)
    set_password = db.Column(db.Boolean, nullable=False)
    email_confirmed = db.Column(db.Boolean, nullable=False)

    def __init__(self, username, email, password, set_password=False, email_confirmed=True):
        self.username = username
        self.email = email
        self.password = password
        self.email_confirmed = email_confirmed
        self.set_password = set_password

    def __repr__(self):
        return f'<User {self.username}>'


class Data(db.Model):
    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, content, user):
        self.content = content
        self.user = user

    def __repr__(self):
        return f'<Data {self.content[:20]}>'

