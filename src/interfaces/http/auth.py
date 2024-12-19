from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    """
    User login
    ---
    parameters:
      - in: body
        name: credentials
        schema:
          type: object
          properties:
            username:
              type: string
              example: admin
            password:
              type: string
              example: secret
    responses:
      200:
        description: JWT access token returned
      401:
        description: Invalid credentials
    """
    data = request.get_json()
    if data.get('username') == 'admin' and data.get('password') == 'secret':
        token = create_access_token(identity='admin_user')
        return jsonify(access_token=token), 200
    return jsonify({"msg": "Bad credentials"}), 401
