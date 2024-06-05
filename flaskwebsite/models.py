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
    password = db.Column(db.String(64), nullable=False)
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
    series = db.Column(db.String(2))
    number = db.Column(db.String(6))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    gender = db.Column(db.String(1))
    place_of_birth = db.Column(db.String(100))
    address = db.Column(db.String(255))
    issued_by = db.Column(db.String(100))
    issue_date = db.Column(db.Date)
    expiry_date = db.Column(db.Date)
    nationality = db.Column(db.String(20))
    personal_numerical_code = db.Column(db.String(13))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, fields, user):
        self.series = fields["series"]
        self.number = fields["number"]
        self.first_name = fields["first_name"]
        self.last_name = fields["last_name"]
        self.gender = fields["gender"]
        self.place_of_birth = fields["place_of_birth"]
        self.address = fields["address"]
        self.issued_by = fields["issued_by"]
        self.issue_date = datetime.strptime(fields["issue_date"], "%d.%m.%y")
        self.expiry_date = datetime.strptime(fields["expiry_date"], "%d.%m.%Y")
        self.nationality = fields["nationality"]
        self.personal_numerical_code = fields["personal_numerical_code"]
        self.user = user

    def __repr__(self):
        return f'<Data {self.content[:20]}>'

