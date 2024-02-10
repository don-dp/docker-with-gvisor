from flask import Flask, request, jsonify
from celery_config import run_container
from helpers import run_container_logic
import os

app = Flask(__name__)
app.config['DEBUG'] = os.environ.get('FLASK_ENV') == 'development'

@app.route('/hello', methods=['GET'])
def hello():
    debug_mode = 'on' if app.debug else 'off'
    return {'message': 'Updated on feb 10 2024', 'debug': debug_mode}

@app.route('/runfunction/<session_id>', methods=['POST'])
def run_function(session_id):
    token = request.headers.get('Authorization')
    if not token:
        response = jsonify({'error': 'Token is missing'})
        response.status_code = 401
        return response

    data = request.get_json()
    task = run_container.delay(data, session_id, token)
    return jsonify({'message': 'Task accepted', 'task_id': str(task.id)}), 202

@app.route('/runfunction_sync/<session_id>', methods=['POST'])
def run_function_sync(session_id):
    if not app.debug:
        return jsonify({'error': 'Endpoint only available in debug mode'}), 403

    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Token is missing'}), 401

    data = request.get_json()
    response = run_container_logic(data)
    return jsonify(response), 200