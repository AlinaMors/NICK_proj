# файл models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
# для взаимодействия с базой данных

# Представляет пользователя в системе
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # nullable - обязательная.
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

# Представляет задачу, созданную пользователем.
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    #  Идентификатор пользователя, создавшего задачу, внешняя ссылка на таблицу User, обязательное поле.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # created_at: Время создания задачи, по умолчанию устанавливается текущее время.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class MapData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Social(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #  Идентификатор пользователя, внешний ключ, ссылающийся на таблицу User, обязательное поле.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class HistoricalPlace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'description': self.description,
        }
    


class Media(db.Model):
    __tablename__ = 'media'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(250), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'type': self.type,
            'task_id': self.task_id
        }

