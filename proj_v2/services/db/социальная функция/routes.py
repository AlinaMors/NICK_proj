from flask import Blueprint, request, jsonify
from models import db, User, Friend, Achievement, Challenge

bp = Blueprint('api', __name__)  # Создание Blueprint для группировки маршрутов.

# Эндпоинт для добавления друга.
@bp.route('/friends', methods=['POST'])
def add_friend():
    data = request.get_json()  # Получение данных запроса в формате JSON.
    new_friend = Friend(user_id=data['user_id'], friend_id=data['friend_id'], status='pending')
    db.session.add(new_friend)  # Добавление нового друга в сессию базы данных.
    db.session.commit()  # Сохранение изменений в базе данных.
    return jsonify({'message': 'Friend request sent'}), 201  # Возвращение ответа.

# Эндпоинт для получения списка друзей.
@bp.route('/friends/<int:user_id>', methods=['GET'])
def get_friends(user_id):
    friends = Friend.query.filter_by(user_id=user_id, status='accepted').all()  # Получение списка друзей пользователя.
    return jsonify([{'id': friend.id, 'friend_id': friend.friend_id} for friend in friends]), 200  # Возвращение списка друзей.

# Эндпоинт для создания вызова.
@bp.route('/challenges', methods=['POST'])
def create_challenge():
    data = request.get_json()
    new_challenge = Challenge(
        title=data['title'],
        description=data['description'],
        user_id=data['user_id'],
        competitor_id=data['competitor_id']
    )
    db.session.add(new_challenge)
    db.session.commit()
    return jsonify({'message': 'Challenge created'}), 201

# Эндпоинт для получения списка вызовов пользователя.
@bp.route('/challenges/<int:user_id>', methods=['GET'])
def get_challenges(user_id):
    challenges = Challenge.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': challenge.id,
        'title': challenge.title,
        'description': challenge.description,
        'status': challenge.status,
        'timestamp': challenge.timestamp
    } for challenge in challenges]), 200

# Эндпоинт для добавления достижения.
@bp.route('/achievements', methods=['POST'])
def add_achievement():
    data = request.get_json()
    new_achievement = Achievement(
        user_id=data['user_id'],
        title=data['title'],
        description=data['description']
    )
    db.session.add(new_achievement)
    db.session.commit()
    return jsonify({'message': 'Achievement added'}), 201

# Эндпоинт для получения списка достижений пользователя.
@bp.route('/achievements/<int:user_id>', methods=['GET'])
def get_achievements(user_id):
    achievements = Achievement.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': achievement.id,
        'title': achievement.title,
        'description': achievement.description,
        'timestamp': achievement.timestamp
    } for achievement in achievements]), 200
