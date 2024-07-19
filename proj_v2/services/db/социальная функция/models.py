from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Первичный ключ.
    username = db.Column(db.String(80), unique=True, nullable=False)  # Имя, не пустое.
    friends = db.relationship('Friend', backref='user', lazy=True)  # Связь с таблицей друзей.

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Внешний ключ, связывающий с пользователем.
    friend_id = db.Column(db.Integer, nullable=False)  # ID друга.
    status = db.Column(db.String(20), nullable=False, default='pending')  # Статус дружбы 'pending', 'accepted'.

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Внешний ключ, связывающий с пользователем.
    title = db.Column(db.String(120), nullable=False)  
    description = db.Column(db.String(250), nullable=True)  # Описание достижения.
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Время создания.

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)  # Название вызова.
    description = db.Column(db.String(250), nullable=True)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Внешний ключ, связывающий с пользователем.
    competitor_id = db.Column(db.Integer, nullable=False)  # ID конкурента.
    status = db.Column(db.String(20), nullable=False, default='pending')  # Статус вызова.
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Время создания.