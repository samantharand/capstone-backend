from flask import Flask, jsonify

DEBUG=True
PORT=8000

app = Flask(__name__)

@app.route('/', methods=['GET'])
def test_route():
	print('yay yay yay');
	return "check the term, gurl"

if __name__ == '__main__':
	app.run(debug=DEBUG, port=PORT)