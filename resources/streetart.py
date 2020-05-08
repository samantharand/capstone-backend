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

@streetart.route('/map', methods=['GET'])
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

# show page
@streetart.route('/<id>', methods=['GET'])
def get_streetart_details(id):
	streetart = models.StreetArt.get(models.StreetArt.id == id)

	streetart_dict = model_to_dict(streetart)
	streetart_dict['poster'].pop('password')

	return jsonify (
		data = streetart_dict,
		message = f'Displaying artwork: {streetart_dict["name"]}, ID{streetart_dict["id"]}',
		status = 200
	), 200

# edit
@streetart.route('/<id>', methods=['PUT'])
@login_required
def edit_streetart_post(id):
	payload = request.get_json()
	streetart_to_edit = models.StreetArt.get(models.StreetArt.id == id)

	if current_user.id == streetart_to_edit.poster.id:
		streetart_to_edit.name = payload['name']
		streetart_to_edit.location = payload['location']
		streetart_to_edit.year = payload['year']
		streetart_to_edit.artist = payload['artist']
		streetart_to_edit.description = payload['description']
		
		streetart_to_edit.save()
		streetart_to_edit_dict = model_to_dict(streetart_to_edit)
		streetart_to_edit_dict['poster'].pop('password')
		return jsonify(
			data = streetart_to_edit_dict,
			message = 'Streetart has been edited',
			status = 201
		), 201

	else:

		return jsonify(
			data = {},
			message = "User cannot edit posts that are not theirs",
			status = 403
		), 403

# delete 
@streetart.route('/<id>', methods=['DELETE'])
def delete_streetart_post(id):
	streetart_to_delete = models.StreetArt.get(models.StreetArt.id == id)

	if current_user.id == streetart_to_delete.poster.id:
		return "ya dis is urs"
	else:
		return "no no no not so fast"
















