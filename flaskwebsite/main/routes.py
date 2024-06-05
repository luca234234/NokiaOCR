import requests
from flask import request, jsonify, Blueprint
from flask_login import login_required, current_user
from flaskwebsite.models import Data
from flaskwebsite.main.utils import extract_data, format_data, field_mapping
from flaskwebsite import db

main = Blueprint('main', __name__)

FASTAPI_OCR_URL = 'http://aiserver:5036/predict/'


@main.route('/ocr-photo', methods=['POST'])
@login_required
def ocr_photo():
    if 'photo' not in request.files:
        return jsonify({'message': 'No photo provided', 'status': 'error'}), 400

    file = request.files['photo']
    if file.filename == '':
        return jsonify({'message': 'No photo selected', 'status': 'error'}), 400

    try:
        files = {'file': (file.filename, file.stream, file.content_type)}
        response = requests.post(FASTAPI_OCR_URL, files=files)

        if response.status_code != 200:
            return jsonify({'message': 'OCR failed', 'status': 'error'}), response.status_code

        ocr_result = response.json()
        fields = extract_data(ocr_result)
        post = Data(fields=fields, user=current_user)
        db.session.add(post)
        db.session.commit()
        return jsonify({'message': 'OCR success', 'status': 'ok', 'data': [{'content': format_data(post), 'created_at': post.created_at.isoformat()}]}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': str(e), 'status': 'error'}), 500


@main.route('/user-data', methods=['GET'])
@login_required
def send_user_data():
    user = current_user
    if user:
        user_data = [{'content': format_data(data), 'created_at': data.created_at.isoformat()} for data in user.data]
        return jsonify({'message': 'Data fetched successfully', 'status': 'ok', 'data': user_data}), 200
    else:
        return jsonify({'message': 'User not found', 'status': 'error'}), 404


@main.route('/edit-data/<int:data_id>', methods=['PUT'])
@login_required
def edit_data(data_id):
    data = Data.query.get_or_404(data_id)

    if data.user_id != current_user.id:
        return jsonify({'message': 'Permission denied', 'status': 'error'}), 403

    fields = request.json
    try:
        for req_field, model_field in field_mapping.items():
            if req_field in fields and fields[req_field]:
                setattr(data, model_field, fields[req_field])

        db.session.commit()
        return jsonify({'message': 'Data updated successfully', 'status': 'ok', 'data': format_data(data)}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': str(e), 'status': 'error'}), 500


@main.route('/delete-data/<int:data_id>', methods=['DELETE'])
@login_required
def delete_data(data_id):
    data = Data.query.get_or_404(data_id)

    if data.user_id != current_user.id:
        return jsonify({'message': 'Permission denied', 'status': 'error'}), 403

    try:
        db.session.delete(data)
        db.session.commit()
        return jsonify({'message': 'Data deleted successfully', 'status': 'ok'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': str(e), 'status': 'error'}), 500
