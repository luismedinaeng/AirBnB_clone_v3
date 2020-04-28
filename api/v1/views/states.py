#!/usr/bin/python3
"""
Index
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """
    Return a list of all states
    """
    states = storage.all(State).values()
    return jsonify([obj.to_dict() for obj in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def ret_state(state_id):
    """
    Return a state
    """
    states = storage.get(State, state_id)
    if states:
        return jsonify(states.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """
    Delete a state
    """
    states = storage.get(State, state_id)
    if states:
        states.delete()
        storage.save()
    else:
        abort(404)
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Create a state
    """
    try:
        state = request.get_json()
    except:
        abort(400, "Not a JSON")
    if "name" not in state:
        abort(400, "Missing name")
    new_state = State(**state)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    update a state
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, description="Not a Json")
    for key, value in body.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
