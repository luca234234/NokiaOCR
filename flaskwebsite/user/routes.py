import random
import string
from flask import request, jsonify, current_app, Blueprint
from utils import hash_password, validate_email, validate_username, send_verification_email
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from itsdangerous import URLSafeTimedSerializer
from flaskwebsite import db, oauth

user = Blueprint('user', __name__)


@user.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=3600)  # 1 hour validity
        user = User.query.filter_by(email=email).first()
        user.email_confirmed = True
        db.session.commit()
        return jsonify({'message': 'Email verified successfully'}), 200
    except:
        return jsonify({'message': 'The verification link is invalid or has expired.'}), 400


@user.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required', 'status': 'error'}), 400

    if validate_username(username):
        return jsonify({'message': 'Username already exists', 'status': 'error'}), 409

    if validate_email(email):
        return jsonify({'message': 'Email already exists', 'status': 'error'}), 409

    hashed_password = hash_password(password)
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    send_verification_email(email, username)
    return jsonify({'message': 'User registered successfully', 'status': 'ok'}), 201


@user.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    hashed_password = hash_password(password)

    user = User.query.filter_by(email=email).first()

    if user and user.password == hashed_password:
        if not user.email_confirmed:
            send_verification_email(user.email, user.username)
            return jsonify({'message': 'Please verify your email', 'status': 'email_not_verified'}), 403
        else:
            login_user(user)
            return jsonify({'message': 'Login successful', 'status': 'ok'}), 200
    else:
        return jsonify({'message': 'Login failed', 'status': 'error'}), 401


@user.route('/google-authorize', methods=['POST'])
def authorize():
    token_json = request.json
    token = token_json.get('token')
    resp = oauth.google.get('userinfo', token={'access_token': token})
    user_info = resp.json()
    email = user_info['email']
    username = user_info['name']
    if validate_email(email):
        user = User.query.filter_by(email=email).first()
        login_user(user)
        if user.set_password:
            return jsonify({'message': 'Please set your password', 'status': 'password_not_set'}), 200
        else:
            return jsonify({'message': 'Login successful', 'status': 'ok'}), 200
    while validate_username(username):
        username = username + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

    password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    user = User(username=username, email=email, password=password, set_password=True)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully', 'status': 'ok'}), 201


@user.route('/update-password', methods=['POST'])
@login_required
def update_password():
    data = request.json
    new_password = data.get('password')

    if not new_password:
        return jsonify({'message': 'Password is required', 'status': 'error'}), 400

    try:
        hashed_password = hash_password(new_password)
        current_user.password = hashed_password
        db.session.commit()
        return jsonify({'message': 'Password updated successfully', 'status': 'ok'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to update password', 'status': 'error', 'error': str(e)}), 500


@user.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful', 'status': 'ok'}), 200

