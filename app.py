from flask import Flask, jsonify
from flask_login import LoginManager
from resources.users import users
from resources.streetart import streetart
from flask_cors import CORS

import models

DEBUG=True
PORT=8000

app = Flask(__name__)

# LOGIN MANAGER
app.secret_key = "top secret key"
login_manager = LoginManager()
login_manager.init_app(app)

# SESSION
@login_manager.user_loader
def load_user(user_id):
	try:
		return models.User.get_by_id(user_id)
	except models.DoesNotExist:
		return None

# AUTH
@login_manager.unauthorized_handler
def unauthoried():
	return jsonify(
		data = {
			'ERROR': 'user not logged in'
		},
		message = 'You have to be logged in to do that!',
		status = 404
	), 404

CORS(users, origins=['http://localhost:3000'], supports_credentials=True)
CORS(streetart, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(streetart, url_prefix='/streetart')

@app.route('/', methods=['GET'])
def test_route():
	print('yay yay yay');
	return "check the term, gurl"

if __name__ == '__main__':
	models.init()
	app.run(debug=DEBUG, port=PORT)