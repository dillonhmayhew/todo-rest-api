from flask import url_for


def make_public_task(task):
    new_task = {}

    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('main.get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]

    return new_task