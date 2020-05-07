from flask import Flask, jsonify
from resources.users import users

import models

DEBUG=True
PORT=8000

app = Flask(__name__)

app.register_blueprint(users, url_prefix='/users/')

@app.route('/', methods=['GET'])
def test_route():
	print('yay yay yay');
	return "check the term, gurl"

if __name__ == '__main__':
	models.init()
	app.run(debug=DEBUG, port=PORT)