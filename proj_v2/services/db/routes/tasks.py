# файл tasks.py
# Этот код создает REST API для управления задачами, включая операции чтения, создания, обновления и удаления задач


# Flask, Flask-RestPlus, SQLAlchemy для работы с базой данных
#  Flask-JWT-Extended для аутентификации с помощью JWT (JSON Web Tokens).


# request и jsonify из Flask используются для работы с HTTP запросами и формирования ответов в формате JSON.
from flask import request, jsonify

# Namespace, Resource, fields из flask_restx используются для создания REST API, определения моделей данных и ресурсов.
from flask_restx import Namespace, Resource, fields

# Task и db импортируются из модуля models для работы с объектами задач и базой данных SQLAlchemy.
from models import Task, db

# jwt_required и get_jwt_identity из flask_jwt_extended используются для защиты маршрутов с помощью JWT и получения идентификационных данных текущего пользователя
from flask_jwt_extended import jwt_required, get_jwt_identity

# tasks_ns создает Namespace для управления задачами с описанием 
tasks_ns = Namespace('tasks', description='Task management')

task_model = tasks_ns.model('Task', {
    'title': fields.String(required=True, description='The task title'),
    
    # fields.String для заголовка и описания задачи.
    'description': fields.String(description='The task description'),
})

# Класс TaskList для работы с коллекцией задач (/tasks):
@tasks_ns.route('/tasks')
class TaskList(Resource):
    # get(self): Метод для получения всех задач текущего пользователя. Использует jwt_required() для защиты маршрута
    @jwt_required()
    def get(self):
        # Идентификация текущего пользователя извлекается с помощью get_jwt_identity()
        user = get_jwt_identity()
        # запрос к БД  для извлечения всех задач пользователя
        tasks = Task.query.filter_by(user_id=user['id']).all()
        # возвращается список задач в формате JSON.
        return jsonify([task.to_dict() for task in tasks])

    @tasks_ns.expect(task_model)
    # task_model в вашем случае представляет собой модель данных, описывающую формат данных, которые ожидаются в запросе к API.
    # указывает, что для данного метода API (в данном случае для метода post() в классе TaskList), ожидается, что клиент отправит данные в том же формате, что и определено в task_model.
    @jwt_required()
    # post(self): Метод для создания новой задачи.
    def post(self):
        data = request.get_json()
        user = get_jwt_identity()
        new_task = Task(title=data['title'], description=data.get('description'), user_id=user['id'])
        # Создает новый объект задачи на основе полученных данных и сохраняет его в базе данных SQLAlchemy.
        
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task created successfully'})


# Класс TaskResource для работы с отдельной задачей (/tasks/<int:task_id>):
@tasks_ns.route('/tasks/<int:task_id>')
class TaskResource(Resource):
    @jwt_required()
    def put(self, task_id):
        data = request.get_json()
        task = Task.query.get(task_id)
        #  находит задачу в базе данных по task_id, обновляет её поля (если задача существует) и сохраняет изменения в базе данных
        if task:
            task.title = data['title']
            task.description = data.get('description')
            db.session.commit()
            return jsonify({'message': 'Task updated successfully'})
        return jsonify({'message': 'Task not found'}), 404

    @jwt_required()
    def delete(self, task_id):
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
            return jsonify({'message': 'Task deleted successfully'})
        return jsonify({'message': 'Task not found'}), 404
