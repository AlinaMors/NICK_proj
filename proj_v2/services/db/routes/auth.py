# файл auth.py
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
# Используются для хеширования пароля при регистрации и проверки пароля при входе.
from flask_jwt_extended import create_access_token, jwt_required
# для создания JWT-токена доступа и обеспечения защищенного доступа к API.

auth_ns = Namespace('auth', description='User authentication')

# Модель данных для регистрации (user_model)
user_model = auth_ns.model('User', {
    'username': fields.String(required=True, description='The username'),
    'email': fields.String(required=True, description='The email address'),
    'password': fields.String(required=True, description='The user password'),
})

# Модель данных для входа (login_model)
login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='The email address'),
    'password': fields.String(required=True, description='The user password'),
})

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(user_model)
    def post(self):
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(username=data['username'], email=data['email'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'})

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'message': 'Invalid credentials'}), 401
        # создает JWT-токен доступа с помощью create_access_token и возвращает его в JSON-ответе.
        access_token = create_access_token(identity={'username': user.username, 'email': user.email})
        return jsonify({'token': access_token})
