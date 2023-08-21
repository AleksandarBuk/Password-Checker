from celery import Celery

celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='rpc'
)

celery_app.conf.task_routes = {
    'your_module.pwned_api_check': {'queue': 'pwned_queue'}
}