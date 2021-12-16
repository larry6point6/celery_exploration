from time import sleep

from celery import Celery

celery = Celery(
    "worker", backend="redis://localhost:6379", broker="redis://localhost:6379"
)


@celery.task()
def add(x, y):
    sleep(100)
    return x + y
