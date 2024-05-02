#!/usr/bin/python3
""" The Start Point For our project """
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ return the status of API in json format """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_count_of_the_values():
    """ return the number of each type """
    classes = [
        Amenity,
        City,
        Place,
        Review,
        State,
        User
    ]

    names = [
        "amenities",
        "cities",
        "places",
        "reviews",
        "states",
        "users"
    ]

    objects = {
        names[i]: storage.count(classes[i]) for i in range(len(classes))
    }

    return jsonify(objects)
