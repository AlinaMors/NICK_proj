from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

GEOCODER_API_SERVER = "http://geocode-maps.yandex.ru/1.x/"
API_KEY = "40d1649f-0493-4b70-98ba-98533de7710b"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/parks', methods=['GET'])
def get_parks():
    location = request.args.get('location')
    geocoder_params = {
        "apikey": API_KEY,
        "geocode": location,
        "format": "json"
    }
    response = requests.get(GEOCODER_API_SERVER, params=geocoder_params)
    if response.status_code == 200:
        # Обработка данных
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

@app.route('/api/recycling_centers', methods=['GET'])
def get_recycling_centers():
    location = request.args.get('location')
    geocoder_params = {
        "apikey": API_KEY,
        "geocode": location,
        "format": "json"
    }
    response = requests.get(GEOCODER_API_SERVER, params=geocoder_params)
    if response.status_code == 200:
        # Обработка данных
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

if __name__ == '__main__':
    app.run(debug=True)
