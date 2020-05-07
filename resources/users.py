import models

from flask import Blueprint, request, jsonify
from flask_login import login_user
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict

users = Blueprint('users', 'users')

@users.route('/', methods=['GET'])
def test_user_route():
	print('User test route :)')
	return "check terminal"

@users.route('/register', methods=['POST'])
def register():
	payload = request.get_json()
	payload['username'] = payload['username'].lower()
	payload['email'] = payload['email'].lower()
	print(payload)

	# see if username is already registered
	try:
		models.User.get(models.User.username == payload['username'])
		
		return jsonify(
			data = {},
			message = "Sorry, that username is already registered :(",
			status = 401
		), 401

	except models.DoesNotExist:
		# see if email is already registered
		try:
			models.User.get(models.User.email == payload['email'])

			return jsonify(
				data = {},
				message = "Sorry, that email is already registered :(",
				status = 401
			), 401

		except models.DoesNotExist:

			created_user = models.User.create(
				username=payload['username'],
				email=payload['email'],
				password=generate_password_hash(payload['password']),
				zip_code=payload['zip_code'],
				bio=payload['bio'],
			)

			print('created_user', created_user)
			
			login_user(created_user)

			created_user_dict = model_to_dict(created_user)
			print('created_user_dict - prepop', created_user_dict)
			created_user_dict.pop('password')

			return jsonify(
				data = created_user_dict,
				message = 'User Created',
				status = 201
			), 201
