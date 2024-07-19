# файл historical.py
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from models import HistoricalPlace, db
from flask_jwt_extended import jwt_required, get_jwt_identity

historical_ns = Namespace('historical', description='Historical Places Management')

# Модель данных для исторической достопримечательности (historical_place_model)
historical_place_model = historical_ns.model('HistoricalPlace', {
    'name': fields.String(required=True, description='The name of the historical place'),
    'location': fields.String(required=True, description='The location of the historical place'),
    'description': fields.String(description='The description of the historical place'),
})

@historical_ns.route('/places')
class HistoricalPlaceList(Resource):
    @jwt_required()
    def get(self):
        places = HistoricalPlace.query.all()
        return jsonify([place.to_dict() for place in places])

    @historical_ns.expect(historical_place_model)
    @jwt_required()
    def post(self):
        data = request.get_json()
        new_place = HistoricalPlace(
            name=data['name'],
            location=data['location'],
            description=data.get('description')
        )
        db.session.add(new_place)
        db.session.commit()
        return jsonify({'message': 'Historical place added successfully'})

@historical_ns.route('/places/<int:place_id>')
class HistoricalPlaceResource(Resource):
    @jwt_required()
    def get(self, place_id):
        place = HistoricalPlace.query.get(place_id)
        if place:
            return jsonify(place.to_dict())
        return jsonify({'message': 'Historical place not found'}), 404

    @jwt_required()
    def put(self, place_id):
        data = request.get_json()
        place = HistoricalPlace.query.get(place_id)
        if place:
            place.name = data['name']
            place.location = data['location']
            place.description = data.get('description')
            db.session.commit()
            return jsonify({'message': 'Historical place updated successfully'})
        return jsonify({'message': 'Historical place not found'}), 404

    @jwt_required()
    def delete(self, place_id):
        place = HistoricalPlace.query.get(place_id)
        if place:
            db.session.delete(place)
            db.session.commit()
            return jsonify({'message': 'Historical place deleted successfully'})
        return jsonify({'message': 'Historical place not found'}), 404
