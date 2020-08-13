from app import db, auth_
from flask import jsonify, abort, request
from app.models import Task
from app.utils.helpers import make_public_task
from app.main import bp


@bp.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth_.login_required
def get_tasks():
    user = auth_.current_user()
    tasks = Task.serialize_list(user.tasks.all())

    return jsonify(tasks=[make_public_task(task) for task in tasks])


@bp.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        abort(404)
    
    return jsonify(task=make_public_task(task.serialize()))


@bp.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    
    task = Task(title=request.json['title'],
                description=request.json.get('description', ''))
    
    db.session.add(task)
    db.session.commit()

    return jsonify(task=make_public_task(task.serialize())), 201


@bp.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) is not str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)

    task.title = request.json.get('title', task.title)
    task.description = request.json.get('description', task.description)
    task.done = request.json.get('done', task.done)

    db.session.add(task)
    db.session.commit()

    return jsonify(task=make_public_task(task.serialize()))


@bp.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        abort(404)

    db.session.delete(task)
    db.session.commit()

    return jsonify(result=True)