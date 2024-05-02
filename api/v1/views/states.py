#!/usr/bin/python3
""" objects that handle all default RestFul API actions for States """
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def index():
    """
    return list of all states
    """
    return jsonify([state.to_dict() for state in storage.all(State).values()])


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create():
    """
    create a new state based on the values in the request body
    """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")

    newState = State(**data)
    newState.save()
    return make_response(jsonify(newState.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def show(state_id):
    """ Get the state by id """
    state = storage.get(State, state_id)
    return jsonify(state.to_dict()) if state else abort(404)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update(state_id):
    """
    Updates a State
    """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)

    storage.save()
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def destroy(state_id):
    """
    Deletes a State Object
    """

    state = storage.get(State, state_id)

    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)
