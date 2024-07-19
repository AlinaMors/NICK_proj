from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)
BASE_URL = '/ya_map'
app.config['BASE_URL'] = BASE_URL
GEOCODER_API_SERVER = "http://geocode-maps.yandex.ru/1.x/"
API_KEY = "40d1649f-0493-4b70-98ba-98533de7710b"


@app.context_processor
def inject_base_url():
    return dict(base_url=BASE_URL)


@app.route('/ya_map')
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


@app.route('/api/location_by_coords', methods=['GET'])
def location_by_coords():
    lat = request.args.get('lat')
    lon = request.args.get('long')
    response = requests.get(f"https://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&geocode={lon},{lat}&format=json")
    if response.status_code == 200:
        location = response.json()['response']['GeoObjectCollection']['featureMember'][0]
        exact_location = location['GeoObject']['description'] +","+ location['GeoObject']['name']
        response = {"location":exact_location}
        return jsonify(response)
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500


if __name__ == '__main__':
    app.run(debug=True)
