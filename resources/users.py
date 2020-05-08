import models

from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
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

		user_dict = model_to_dict(user)
		print("USER DICT", user_dict)
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

@users.route('/logout', methods=['GET'])
def logout():
	logout_user()
	return jsonify(
		data = {},
		message = "User has logged out",
		status = 200
	), 200

# all users in database
@users.route('/all', methods=['GET'])
@login_required
def get_all_users():
	users = models.User.select()

	user_dicts = [model_to_dict(user) for user in users]

	for user_dict in user_dicts:
		user_dict.pop('password')

	return jsonify(
		data = user_dicts,
		message = f'Showing all users in database - {len(user_dicts)} total',
		status = 200
	), 200

# get details of one account
@users.route('/<id>', methods=['GET'])
def get_user_details(id):
	user = models.User.get(models.User.id == id)

	user_dict = model_to_dict(user)
	user_dict.pop('password')



	return jsonify(
		data = user_dict,
		message = f'Showing account details for user: {user_dict["username"]}, ID#{user_dict["id"]}',
		status = 200
	), 200

# edit
@users.route('/<id>', methods=['PUT'])
def edit_user_details():
	payload = request.get_json()

#destroy













