#!/usr/bin/python3
""" The Start Point For our project """
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ return the status of API in json format """
    return jsonify({"status": "OK"})
