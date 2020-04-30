#!/usr/bin/python3
"""
Index
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Return a Json with status OK
    Endpoint that check the status fo the API
    ---
    tags:
      - index
    produces:
      - application/json
    responses:
      200:
        description: Success connection
        schema:
          id: Status
          properties:
            status:
              type: string
              description: Status connection
              example: OK
    """
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """
    Return the number of each objects by type
    Return the number of the objects managed by the API such as Amenity,
    City, Place, Review, State, User
    ---
    tags:
      - index
    produces:
      - application/json
    responses:
      200:
        description: Succesful operation
        schema:
          id: Stats
          properties:
            amenities:
              type: int
              description: Number of Amenity objects
              example: 10
            cities:
              type: int
              description: Number of City objects
              example: 8
            places:
              type: int
              description: Number of Place objects
              example: 24
            reviews:
              type: int
              description: Number of Review objects
              example: 42
            states:
              type: int
              description: Number of States objects
              example: 3
            users:
              type: int
              description: Number of User objects
              example: 35
    """
    return jsonify(amenities=storage.count("Amenity"),
                   cities=storage.count("City"),
                   places=storage.count("Place"),
                   reviews=storage.count("Review"),
                   states=storage.count("State"),
                   users=storage.count("User"))
