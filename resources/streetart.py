import models

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict


streetart = Blueprint('streetart', 'streetart')

@streetart.route('/', methods=['GET'])
def test_route():
	return "streetart route reached"

@streetart.route('/add', methods=['POST'])
@login_required
def add_streetart():
	payload = request.get_json()

	created_streetart = models.StreetArt.create(
		name = payload['name'],
		location = payload['location'],
		year = payload['year'],
		artist = payload['artist'],
		description = payload['description'],
		poster = current_user.id
	)

	created_streetart_dict = model_to_dict(created_streetart)
	created_streetart_dict['poster'].pop('password')

	return jsonify(
		data = created_streetart_dict,
		message = 'Successfully created a Streetart Post',
		status = 201
	), 201

@streetart.route('/all', methods=['GET'])
def get_all_streetart():
	streetart = models.StreetArt.select()

	streetart_dicts = [model_to_dict(streetart) for streetart in streetart]
	for streetart_dict in streetart_dicts:
		streetart_dict['poster'].pop('password')

	return jsonify(
		data = streetart_dicts,
		message = f'Found all street art in database - {len(streetart_dicts)} total.',
		status = 200
	), 200


