from time import sleep

from celery import Celery

celery = Celery(
    "worker", backend="redis://localhost:6379", broker="redis://localhost:6379"
)


@celery.task()
def add_task(x, y):
    sleep(15)
    return x + y
