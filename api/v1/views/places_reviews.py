#!/usr/bin/python3
"""
Index
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.review import Review

@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def places_reviews(state_id):
    place = storage.get(Place, place_id)
    if place:
        return jsonify([obj.to_dict() for obj in place.reviews])
    else:
        abort(404)

@app_views.route('/reviews/<review_id>', methods=['GET'])
def ret_review(review_id):
    """
    Return a review
    """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """
    Delete a review
    """
    review = storage.get(Review, review_id)
    if review:
        review.delete()
        storage.save()
    else:
        abort(404)
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """
    Create a review
    """
    place = storage.get(Place, place_id)
    if not state:
        abort(404)
    try:
        review = request.get_json()
    except:
        abort(400, "Not a JSON")
    if "user_id" not in review:
        abort(400, "Missing user_id")
    user = review['user_id']
    if not storage.get("User", user):
        abort(404)
    if "text" not in review:
        abort(400, "Missing text")
    new_review = Review(**review)
    setattr(new_review, 'place_id', place_id)
    storage.new(new_review)
    storage.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    update a review
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, description="Not a Json")
    for key, value in body.items():
        if key not in ['id', 'created_at', 'updated_at', 'user_id', 'place_id']:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
