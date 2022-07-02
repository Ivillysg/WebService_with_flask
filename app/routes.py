from crypt import methods
from app import app
from flask import request, jsonify
from app import database


@app.route('/')
def root():
    return 'Hello, World!'


def response_users():
    return {'users': list(database.users_data.values())}


@app.route('/users')
def users():
    return jsonify(response_users()), 200


@app.route('/users', methods=['POST'])
def create_user():
    body = request.json

    ids = list(database.users_data.keys())

    if ids:
        new_id = ids[-1] + 1
    else:
        new_id = 1

    database.users_data[new_id] = {
        'id': new_id,
        'name': body['name'],
    }

    return jsonify(response_users()), 201


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id: int):
    body = request.json

    if user_id not in database.users_data:
        return jsonify({'error': 'User not found'}), 404

    database.users_data[user_id]['name'] = body['name']

    return jsonify({'message': 'User successfully updated', 'user': database.users_data[user_id]}), 200


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int):
    user = database.users_data.get(user_id)
    if user:
        del database.users_data[user_id]
        return jsonify(), 204

    return jsonify({'error': 'User not found'}), 404
