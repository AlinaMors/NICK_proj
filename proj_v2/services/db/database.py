# файл database.py
# инициализацию базы данных для приложения Flask, используя SQLAlchemy
from flask import Flask
# из Flask для создания веб-приложения.
from models import db

def init_db(app):
    # Инициализация приложения с SQLAlchemy:
    db.init_app(app)
    with app.app_context():
        # Создает все таблицы, определенные в моделях SQLAlchemy, 
        db.create_all()