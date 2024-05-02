#!/usr/bin/python3
""" API For cities """
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def index(state_id):
    """
    return list of all cities depend on the state_id
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    
    list_cities = [city.to_dict() for city in state.cities]
    return make_response(jsonify(list_cities), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def store(state_id):
    """
    Create a new city
    """

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")

    data['state_id'] = state.id
    newCity = City(**data)
    newCity.save()
    return make_response(jsonify(newCity.to_dict()), 201)


@app_views.route('/cities/<city_id>/', methods=['GET'], strict_slashes=False)
def show(city_id):
    """
    Get City By ID
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return make_response(jsonify(city.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update(city_id):
    """
    Update the city
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def destroy(city_id):
    """
    Delete the city
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)
    
    storage.delete(city)
    return make_response(jsonify({}), 200)
