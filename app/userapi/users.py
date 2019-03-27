from flask import jsonify, request, url_for
from app.models import User
from app.userapi import bp
from app.userapi.errors import bad_request


@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
        user = User.find_by_id(id)
        if user:
            user.delete_from_db()
        return jsonify({'message': 'store deleted'}), 200


@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data:
        return bad_request('must include username and email')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data)
    user.add_to_db()
    response = jsonify(user.to_dict())
    response.headers['Location'] = url_for('userapi.get_user', id=user.id)
    return response, 201


@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data)
    user.update_to_db()
    return jsonify(user.to_dict())


@bp.route('/users', methods=['GET'])
def get_users():
    return jsonify(User.to_collection_dict(User.query.all()))
