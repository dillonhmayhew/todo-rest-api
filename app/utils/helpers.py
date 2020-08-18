from flask import url_for
from app.models import User


def make_public_user(user):
    new_user = {}

    for field in user:
        if field == 'password_hash':
            continue
        if field == 'tasks':
            continue
        if field == 'id':
            user_tasks = User.query.get(user['id']).tasks.all()
            new_user['tasks'] = len(user_tasks)
            new_user['uri'] = url_for('main.get_user', username=user['username'], _external=True)
        else:
            new_user[field] = user[field]

    return new_user


def make_public_task(task):
    new_task = {}

    for field in task:
        if field == 'user_id':
            continue
        if field == 'author':
            continue
        if field == 'id':
            new_task['uri'] = url_for('main.get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]

    return new_task