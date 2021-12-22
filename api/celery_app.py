from time import sleep

from celery import Celery
from celery.contrib import rdb

celery = Celery(
    "worker", backend="redis://localhost:6379", broker="redis://localhost:6379"
)


@celery.task()
def add_task(x, y):
    sleep(10)
    result = x + y
    rdb.set_trace()
    return result
