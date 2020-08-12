from app import app, db
from flask import jsonify
from app.models import Task


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    tasks = [t for t in Task.query.all()]
    print(tasks)
    return jsonify({'tasks': tasks})
