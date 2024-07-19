# файл app.py
from flask import Flask
from config import Config
from database import init_db
from flask_jwt_extended import JWTManager
from flask_restx import Api
from routes.auth import auth_ns
from routes.tasks import tasks_ns
from routes.map import map_ns
from routes.social import social_ns
from routes.historical import historical_ns

app = Flask(__name__)
app.config.from_object(Config)
BASE_URL = '/db'
app.config['BASE_URL'] = BASE_URL 

jwt = JWTManager(app)

init_db(app)

api = Api(app, doc='/docs', title='My API', version='1.0', description='A simple API')

api.add_namespace(auth_ns, path='/auth')
api.add_namespace(tasks_ns, path='/api')
api.add_namespace(map_ns, path='/api')
api.add_namespace(social_ns, path='/api')
api.add_namespace(historical_ns, path='/api')
if __name__ == '__main__':
    app.run(debug=True, port=5001)
