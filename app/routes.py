from app import app, db
from flask import jsonify, abort, request
from app.models import Task


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.serialize_list(Task.query.all())

    return jsonify(tasks=tasks)


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        abort(404)
    
    return jsonify(task=task.serialize())


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    
    task = Task(title=request.json['title'],
                description=request.json.get('description', ''))
    
    db.session.add(task)
    db.session.commit()

    return jsonify(task=task.serialize()), 201

# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
# def update_task(task_id):
