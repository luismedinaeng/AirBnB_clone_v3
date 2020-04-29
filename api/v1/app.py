#!/usr/bin/python3
"""
Main module of web app
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(log):
    """
    Close the connection created to storage
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Manage 'not found' exceptions
    """
    return make_response(jsonify(error="Not found"), 404)


if __name__ == "__main__":
    host = '0.0.0.0' if getenv('HBNB_API_HOST') is None \
        else getenv('HBNB_API_HOST')
    port = 5000 if getenv('HBNB_API_PORT') is None \
        else getenv('HBNB_API_PORT')

    app.run(host=host, port=port, threaded=True, debug=True)
