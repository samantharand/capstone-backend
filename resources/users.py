import models

from flask import Blueprint, request, jsonify

users = Blueprint('users', 'users')

@users.route('/', methods=['GET'])
def test_user_route():
	print('User test route :)')
	return "check terminal"

