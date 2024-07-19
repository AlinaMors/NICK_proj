# как пользоваться post-man


from flask import Flask
from config import Config
from models import db
from routes import bp

app = Flask(__name__)  # Создание экземпляра Flask.
app.config.from_object(Config)  # Загрузка конфигурации.
db.init_app(app)  # Инициализация базы данных.
app.register_blueprint(bp, url_prefix='/api')  # Регистрация маршрутов.

with app.app_context():
    db.create_all()  # Создание таблиц базы данных при запуске приложения.

if __name__ == '__main__':
    app.run(debug=True)  # Запуск приложения в режиме отладки.

