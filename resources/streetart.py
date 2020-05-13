import models
import requests

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
	
	location = '+'.join(payload["location"].split(' '))
	
	print( location )

	geocodeUrl = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + location + '&key=AIzaSyB7G8yZAkGYtf2QQzkS1n0E1gZtpPF_h8w'
	print('geocodeUrl', geocodeUrl)

	response = requests.get(geocodeUrl).json()
	print('-' * 30)
	print("response -->", response)
	print('-' * 30)
	print("response['results'][0]['geometry'] -------", response['results'][0]['geometry'])
	latitude = response['results'][0]['geometry']['location']['lat']
	longitude = response['results'][0]['geometry']['location']['lng']
	print('latitude', latitude)
	print('longitude', longitude)
	# responseJson = jsonify(response.text)
	# print(responseJson)

	

	created_streetart = models.StreetArt.create(
		name = payload['name'],
		latitude = latitude,
		longitude = longitude,
		image = payload['image'],
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


	## 
	
	location = '+'.join(payload["location"].split(' '))
	
	print( location )

	geocodeUrl = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + location + '&key=AIzaSyB7G8yZAkGYtf2QQzkS1n0E1gZtpPF_h8w'
	print('geocodeUrl', geocodeUrl)

	response = requests.get(geocodeUrl).json()
	print('-' * 30)
	print("response -->", response)
	print('-' * 30)
	print("response['results'][0]['geometry'] -------", response['results'][0]['geometry'])
	latitude = response['results'][0]['geometry']['location']['lat']
	longitude = response['results'][0]['geometry']['location']['lng']
	print('latitude', latitude)
	print('longitude', longitude)

	## 

	if current_user.id == streetart_to_edit.poster.id:
		streetart_to_edit.name = payload['name']
		streetart_to_edit.latitude = latitude
		streetart_to_edit.longitude = longitude
		streetart_to_edit.year = payload['year']
		streetart_to_edit.image = payload['image']
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
		streetart_to_delete.delete_instance()

		return jsonify(
			data = {},
			message = "Post successfully deleted."
		)
	else:
		return jsonify(
			data = {},
			message = "User cannot delete posts that are not theirs",
			status = 403
		), 403