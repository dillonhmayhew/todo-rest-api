from app import db, auth_
from flask import jsonify, abort, request, g
from app.models import User, Task
from app.utils.helpers import make_public_task, make_public_user
from app.main import bp


@bp.route('/api/token')
@auth_.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify(token=token.decode('ascii'), duration=600)


@bp.route('/api/users', methods=['GET'])
@auth_.login_required
def get_users():
    users = User.serialize_list(User.query.all())

    return jsonify(users=[make_public_user(user) for user in users])


@bp.route('/api/users/<username>', methods=['GET'])
@auth_.login_required
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    
    return jsonify(user=make_public_user(user.serialize()))


@bp.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        abort(400)
    username = request.json.get('username')
    email = request.json.get('email')
    passwd = request.json.get('passwd')

    if username is None or email is None or passwd is None:
        abort(400)   # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user

    user = User(username=username,
                email=email)
    user.set_password(passwd)
    
    db.session.add(user)
    db.session.commit()

    return jsonify(user=make_public_user(user.serialize())), 201


@bp.route('/api/users/<username>', methods=['PUT'])
@auth_.login_required
def update_user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    if user != g.user:
        abort(401)
    if not request.json:
        abort(400)
    if 'username' in request.json and type(request.json['username']) is not str:
        print("here")
        abort(400)
    if 'email' in request.json and type(request.json['email']) is not str:
        abort(400)
    if 'passwd' in request.json and type(request.json['passwd']) is not str:
        abort(400)

    user.username = request.json.get('username', user.username)
    user.email = request.json.get('email', user.email)

    if 'passwd' in request.json:
        user.set_password(request.json['passwd'])

    db.session.add(user)
    db.session.commit()

    return jsonify(user=make_public_user(user.serialize()))


@bp.route('/api/users/<username>', methods=['DELETE'])
@auth_.login_required
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    if user != g.user:
        abort(401)

    db.session.delete(user)
    db.session.commit()

    return jsonify(result=True)


@bp.route('/api/tasks', methods=['GET'])
@auth_.login_required
def get_tasks():
    user = g.user
    tasks = Task.serialize_list(user.tasks.all())

    return jsonify(tasks=[make_public_task(task) for task in tasks])


@bp.route('/api/tasks/<int:task_id>', methods=['GET'])
@auth_.login_required
def get_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        abort(404)
    if task.author != g.user:
        abort(401)
    
    return jsonify(task=make_public_task(task.serialize()))


@bp.route('/api/tasks', methods=['POST'])
@auth_.login_required
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    
    user = g.user
    task = Task(title=request.json['title'],
                description=request.json.get('description', ''), author=user)
    
    db.session.add(task)
    db.session.commit()

    return jsonify(task=make_public_task(task.serialize())), 201


@bp.route('/api/tasks/<int:task_id>', methods=['PUT'])
@auth_.login_required
def update_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        abort(404)
    if task.author != g.user:
        abort(401)
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


@bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@auth_.login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        abort(404)
    if task.author != g.user:
        abort(401)

    db.session.delete(task)
    db.session.commit()

    return jsonify(result=True)