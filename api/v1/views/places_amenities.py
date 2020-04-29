#!/usr/bin/python3
"""
link between Place objects and Amienity objects
that handles all default RestFul API actions
"""
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def places_amenities(place_id):
    """ List of all amenities in a place """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        lis = [amenity.to_dict() for amenity in place.amenities]
    else:
        lis = [storage.get(Amenity, id).to_dict() for id in place.amenity_ids]
    return jsonify(lis)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def del_pamenities(place_id, amenity_id):
    """ Delete a Amenity """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity not in place.amenities:
            abort(404)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        index = place.amenity_ids.index(amenity_id)
        place.amenity_ids.pop(index)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_pamenities(place_id, amenity_id):
    """ Link Amenity with place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenity_ids.append(amenity_id)
    storage.save()
    return make_Response(jsonify(amenity.to_dict()), 201)
