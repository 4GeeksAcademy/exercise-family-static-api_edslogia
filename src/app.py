"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")

members = [
    {
        "first_name": "John",
        "age": 33,
        "lucky_numbers": [7, 13, 22]
    },
    {
        "first_name": "Jane",
        "age": 35,
        "lucky_numbers": [10, 14, 3]
    },
    {
        "first_name": "Jimmy",
        "age": 5,
        "lucky_numbers": [1]
    }]

jackson_family.add_member(members[0])
jackson_family.add_member(members[1])
jackson_family.add_member(members[2])


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route('/members/<int:id>', methods=['GET'])
def handle_member_id(id):
    member = jackson_family.get_member(id)
    status_code = 400 if member is False else 200
    return jsonify(member), status_code


@app.route('/members', methods=['POST'])
def handle_add_member():
    request_body = request.json
    required_fields = ["first_name", "age", "lucky_numbers"]

    for field in required_fields:
        if field not in request_body:
            return jsonify({"error": f" '{field}' es requerido."}), 400

    if not isinstance(request_body['first_name'], str):
        return jsonify({"error": "'first_name' debe ser un string"}), 400
    if not isinstance(request_body['age'], int):
        return jsonify({"error": "'age' debe ser un entero"}), 400
    if not isinstance(request_body['lucky_numbers'], list):
        return jsonify({"error": "'lucky_numbers' debe ser una lista"}), 400

    member_added = jackson_family.add_member(request_body)
    return jsonify(member_added), 200


@app.route('/members/<int:id>', methods=['DELETE'])
def handle_delete_member(id):
    response = jackson_family.delete_member(id)
    status_code = 200 if response else 400 
    return jsonify({"done": response}), status_code


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)