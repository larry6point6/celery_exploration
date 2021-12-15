from time import sleep

from celery import Celery

celery = Celery("worker", backend="redis://localhost", broker="redis://localhost")


@celery.task()
def add(x, y):
    sleep(10)
    return x + y
