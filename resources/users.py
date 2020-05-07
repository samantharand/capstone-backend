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
	
	# username check
	try:
		models.User.get(models.User.username == payload['username'])
		
		return jsonify(
			data = {},
			message = "Sorry, that username is already registered :(",
			status = 401
		), 401

	except models.DoesNotExist:
		# email check
		try:
			models.User.get(models.User.email == payload['email'])

			return jsonify(
				data = {},
				message = "Sorry, that email is already registered :(",
				status = 401
			), 401	

		except models.DoesNotExist:
			# make account
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

@users.route('/login', methods=['POST'])
def login():
	payload = request.get_json()
	payload['username'] = payload['username'].lower()
	print("Login route, here's payload", payload)

	#username check 
	try:
		user = models.User.get(models.User.username == payload['username'])
		# check password !! remember hash! 

		user_dict = model_to_dict(user)
		print("USER DICT from line 83 in users", user_dict)
		good_password = check_password_hash(user_dict['password'], payload['password'])

		if good_password:

			login_user(user)

			user_dict.pop('password')
			
			return jsonify(
				data = user_dict,
				message = f'Welcome back, {user_dict["username"]}!',
				status = 201
			), 201

		else:
			print('bad password')

			return jsonify(
				data = {},
				message = "Wrong username or password",
				status = 401
			), 401

	except models.DoesNotExist:

		print('bad username')

		return jsonify(
			data = {},
			message = "Wrong username or password",
			status = 401,
		), 401











