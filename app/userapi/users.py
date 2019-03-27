from flask import jsonify, request, url_for
from app import db
from app.models import User
from app.userapi import bp
from app.userapi.errors import bad_request

print('User Routes loading...')

@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    print('route: GET/users/id')
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/users', methods=['POST'])
def create_user():
    print('route: POST/users')
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('userapi.get_user', id=user.id)
    return response


@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    print('route: PUT/users/id')
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())


@bp.route('/users', methods=['GET'])
def get_users():
    print('route: GET/users')
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'userapi.get_users')
    return jsonify(data)
