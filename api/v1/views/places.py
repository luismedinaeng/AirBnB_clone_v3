#!/usr/bin/python3
"""
Place module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place
from models.user import User

@app_views.route('/cities/<city_id>/places', methods=['GET'])
def cities_places(city_id):
    cities = storage.get(City, city_id)
    if cities:
        return jsonify([obj.to_dict() for obj in cities.places])
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'])
def ret_place(place_id):
    """
    Return a place
    """
    places = storage.get(Place, place_id)
    if places:
        return jsonify(places.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """
    Delete a place
    """
    places = storage.get(Place, place_id)
    if places:
        places.delete()
        storage.save()
    else:
        abort(404)
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """
    Create a place
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    try:
        place = request.get_json()
    except:
        abort(400, "Not a JSON")
    if "user_id" not in place:
        abort(400, "Missing user_id")
    user = storage.get(User, place["user_id"])
    if not user:
        abort(404)
    if "name" not in place:
        abort(400, "Missing name")
    place['city_id'] = city.id
    new_place = Place(**place)
    storage.new(new_place)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """
    update a place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    try:
        body = request.get_json()
    except:
        abort(400, description="Not a Json")
    for key, value in body.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
