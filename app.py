from flask import Flask, jsonify
from resources.users import users
from flask_login import LoginManager

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

app.register_blueprint(users, url_prefix='/users/')

@app.route('/', methods=['GET'])
def test_route():
	print('yay yay yay');
	return "check the term, gurl"

if __name__ == '__main__':
	models.init()
	app.run(debug=DEBUG, port=PORT)