#!/usr/bin/python3
"""
Index
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def users():
    """
    Return a list of all users
    """
    users = storage.all(User).values()
    return jsonify([obj.to_dict() for obj in users])


@app_views.route('/users/<user_id>', methods=['GET'])
def ret_user(user_id):
    """
    Return a user
    """
    users = storage.get(User, user_id)
    if users:
        return jsonify(users.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user
    """
    users = storage.get(User, user_id)
    if users:
        users.delete()
        storage.save()
    else:
        abort(404)
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Create a user
    """
    user = request.get_json()
    if not user:
        abort(400, "Not a JSON")
    if "email" not in user:
        abort(400, "Missing email")
    if "password" not in user:
        abort(400, "Missing password")
    new_user = User(**user)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    update a user
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, description="Not a Json")
    for key, value in body.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
