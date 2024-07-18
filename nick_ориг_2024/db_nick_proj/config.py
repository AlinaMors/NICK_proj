# файл confing.py


import os
# взаимодействия с операционной системой, включая доступ к переменным окружения.

# конфигурационных параметров приложения.
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'

    # Получает значение переменной окружения DATABASE_URL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    # Устанавливает параметр SQLALCHEMY_TRACK_MODIFICATIONS в значение False, что отключает функциональность отслеживания изменений объектов. Это улучшает производительность и снижает использование памяти.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #  Этот параметр используется для подписи JSON Web Tokens (JWT) для аутентификации и авторизации.
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your_jwt_secret_key'
