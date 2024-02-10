from celery import Celery
from helpers import send_message, run_container_logic

def make_celery():
    backend = 'redis://redis:6379/0'
    broker = 'redis://redis:6379/0'
    celery = Celery('my_celery_app', backend=backend, broker=broker)
    return celery

celery = make_celery()

@celery.task(soft_time_limit=30, time_limit=40)
def run_container(data, session_id, token):
    response = run_container_logic(data)
    send_message(response, session_id, token)