import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import navigate

application = Flask(__name__)
CORS(application)

@application.route('/', methods=['GET'])
def verify():
    return "Hello from Flask!", 200

@application.route('/', methods=['POST'])
def handle_incoming_messages():
    print('Post request received', file=sys.stderr)
    req_data = request.get_json()
    _lat = req_data["latlong"][0]
    _long = req_data["latlong"][1]
    pickupLocation = str(_lat)+","+str(_long)
    quickestPath = navigate.getQuickestPath(pickup=pickupLocation)
    return jsonify(quickestPath)

if __name__ == '__main__':
    application.run(debug=True)

