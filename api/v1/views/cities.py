#!/usr/bin/python3
"""
Index
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City

@app_views.route('/states/<state_id>/cities', methods=['GET'])
def states_cities(state_id):
    states = storage.get(State, state_id)
    if states:
        return jsonify([obj.to_dict() for obj in states.cities])
    else:
        abort(404)


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def cities():
    """
    Return a list of all cities
    """
    cities = storage.all(City).values()
    return jsonify([obj.to_dict() for obj in cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def ret_city(city_id):
    """
    Return a city
    """
    cities = storage.get(City, city_id)
    if cities:
        return jsonify(cities.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """
    Delete a city
    """
    cities = storage.get(City, city_id)
    if cities:
        cities.delete()
        storage.save()
    else:
        abort(404)
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """
    Create a city
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    try:
        city = request.get_json()
    except:
        abort(400, "Not a JSON")
    if "name" not in city:
        abort(400, "Missing name")
    city['state_id'] = state.id
    new_city = City(**city)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    update a city
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, description="Not a Json")
    for key, value in body.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
