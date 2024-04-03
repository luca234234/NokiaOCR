from flask import request, jsonify, Blueprint
from flask_login import login_required, current_user
import pytesseract
from flaskwebsite.models import Data
from PIL import Image
import io
from flaskwebsite import db

main = Blueprint('main', __name__)


@main.route('/ocr-photo', methods=['POST'])
@login_required
def ocr_photo():
    if 'photo' not in request.files:
        return jsonify({'message': 'No photo provided', 'status': 'error'}), 400

    file = request.files['photo']
    if file.filename == '':
        return jsonify({'message': 'No photo selected', 'status': 'error'}), 400

    try:
        image = Image.open(io.BytesIO(file.read()))
        ocr_result = pytesseract.image_to_string(image)
        post = Data(content=ocr_result, user=current_user)
        db.session.add(post)
        db.session.commit()
        return jsonify({'message': 'OCR success', 'status': 'ok', 'data': ocr_result}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'error'}), 500


@main.route('/user-data', methods=['GET'])
@login_required
def send_user_data():
    user = current_user
    if user:
        user_data = [{'content': data.content, 'created_at': data.created_at.isoformat()} for data in user.data]
        return jsonify({'message': 'Data fetched successfully', 'status': 'ok', 'data': user_data}), 200
    else:
        return jsonify({'message': 'User not found', 'status': 'error'}), 404
