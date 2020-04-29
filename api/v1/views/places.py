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
from models.state import State
from models.amenity import Amenity


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
    place = request.get_json()
    if not place:
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
    body = request.get_json()
    if not body:
        abort(400, description="Not a Json")
    for key, value in body.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'])
def search_place():
    """
    retrieves all Place objects depending of the JSON
    in the body of the request.
    """
    body = request.get_json()
    if body is None:
        abort(400, description="Not a JSON")
    if body and len(body):
        states = body.get('states', None)
        cities = body.get('cities', None)
        amenities = body.get('amenities', None)
    if not body and len(body) or (not states and not cities and not amanities):
        places = storage.all(Place).values()
        place_list = []
        for place in places:
            place_list.append(place.to_dict())
        return jsonify(place_list)
    place_list = []
    if states:
        stateso = [storage.get(State, key) for key in states]
        for state in stateso:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            place_list.append(place)
    if cities:
        cityo = [storage.get(City, key) for key in cities]
        for city in cityo:
            if city:
                for place in city.places:
                    if place not in place_list:
                        place_list.append(place)
    if amenities:
        if not place_list:
            place_list = storage.all(Place).values()
        amenitieso = [storage.get(Amenity, key) for key in amenities]
        place_list = [place for place in place_list
                          if all([key in place.amenities
                                  for key in amenitieso])]
    places = []
    for value in place_list:
        data = value.to_dict()
        data.pop('amenities', None)
        places.append(data)
    return jsonify(places)
