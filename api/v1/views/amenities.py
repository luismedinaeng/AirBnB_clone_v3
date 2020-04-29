#!/usr/bin/python3
"""
Index
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def amenities():
    """
    Return a list of all states
    """
    amenities = storage.all(Amenity).values()
    return jsonify([obj.to_dict() for obj in amenities])


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def ret_amenities(amenity_id):
    """
    Return a amenitie
    """
    amenities = storage.get(Amenity, amenity_id)
    if amenities:
        return jsonify(amenities.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """
    Delete a amenity
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        amenity.delete()
        storage.save()
    else:
        abort(404)
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """
    Create a state
    """
    try:
        amenity = request.get_json()
    except:
        abort(400, "Not a JSON")
    if "name" not in amenity:
        abort(400, "Missing name")
    new_amenity = Amenity(**amenity)
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """
    update a state
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    try:
        body = request.get_json()
    except:
        abort(400, description="Not a Json")
    for key, value in body.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenitie, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
