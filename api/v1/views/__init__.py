#!/usr/bin/python3
"""
Blueprint views
"""
from flask import Blueprint
from api.v1.views import *

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')