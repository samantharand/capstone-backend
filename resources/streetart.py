import models

from flask import Blueprint, jsonify, request

streetart = Blueprint('streetart', 'streetart')

@streetart.route('/', methods=['GET'])
def test_route():
	return "streetart route reached"