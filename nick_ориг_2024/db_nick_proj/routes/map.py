# файл map.py
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from models import MapData, db
from flask_jwt_extended import jwt_required, get_jwt_identity

map_ns = Namespace('map', description='Map data management')

map_model = map_ns.model('MapData', {
    'location': fields.String(required=True, description='The location'),
    'description': fields.String(description='The description'),
})

@map_ns.route('/map')
class MapDataList(Resource):
    @jwt_required()
    def get(self):
        user = get_jwt_identity()
        map_data = MapData.query.filter_by(user_id=user['id']).all()
        return jsonify([data.to_dict() for data in map_data])

    @map_ns.expect(map_model)
    @jwt_required()
    def post(self):
        data = request.get_json()
        user = get_jwt_identity()
        new_map_data = MapData(location=data['location'], description=data.get('description'), user_id=user['id'])
        db.session.add(new_map_data)
        db.session.commit()
        return jsonify({'message': 'Map data created successfully'})

@map_ns.route('/map/<int:data_id>')
class MapDataResource(Resource):
    @jwt_required()
    def put(self, data_id):
        data = request.get_json()
        map_data = MapData.query.get(data_id)
        if map_data:
            map_data.location = data['location']
            map_data.description = data.get('description')
            db.session.commit()
            return jsonify({'message': 'Map data updated successfully'})
        return jsonify({'message': 'Map data not found'}), 404

    @jwt_required()
    def delete(self, data_id):
        map_data = MapData.query.get(data_id)
        if map_data:
            db.session.delete(map_data)
            db.session.commit()
            return jsonify({'message': 'Map data deleted successfully'})
        return jsonify({'message': 'Map data not found'}), 404
