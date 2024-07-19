# файл social.py
# включает методы для получения списка друзей пользователя, добавления нового друга и удаления существующего друга

from flask import request, jsonify
# Namespace из flask_restx используется для создания и организации REST API пространства имен
from flask_restx import Namespace, Resource, fields     #  fields моделей данных
from models import Social, db, User
from flask_jwt_extended import jwt_required, get_jwt_identity

social_ns = Namespace('social', description='Social functions')

# Определение модели данных для друзей
friend_model = social_ns.model('Friend', {
    'friend_id': fields.Integer(required=True, description='The friend user ID'),
})


# Определение ресурса для списка друзей
# @social_ns.route('/friends'): Этот декоратор определяет конечную точку API /friends в рамках пространства имен social_ns.
@social_ns.route('/friends')
class FriendList(Resource):
    @jwt_required()
    def get(self):
        user = get_jwt_identity()
        # запрос для получения списка друзей текущего пользователя
        friends = Social.query.filter_by(user_id=user['id']).all()
        return jsonify([friend.to_dict() for friend in friends])

# что ресурс API, к которому применяется эта аннотация, ожидает получить данные в формате, определенном моделью friend_model
    @social_ns.expect(friend_model)
    @jwt_required()
    def post(self):
        data = request.get_json()
        user = get_jwt_identity()
        # Метод post обрабатывает POST-запрос для добавления нового друга текущему пользователю
        new_friend = Social(user_id=user['id'], friend_id=data['friend_id'])
        db.session.add(new_friend)
        db.session.commit()
        return jsonify({'message': 'Friend added successfully'})

# Определение ресурса для управления отдельным другом 
@social_ns.route('/friends/<int:friend_id>')
class FriendResource(Resource):
    @jwt_required()
    def delete(self, friend_id):
        user = get_jwt_identity()
        friend = Social.query.filter_by(user_id=user['id'], friend_id=friend_id).first()
        if friend:
            db.session.delete(friend)
            db.session.commit()
            return jsonify({'message': 'Friend removed successfully'})
        return jsonify({'message': 'Friend not found'}), 404
