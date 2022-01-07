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
    # fmt: off
    import rpdb; rpdb.Rpdb(addr='0.0.0.0').set_trace()
    # fmt: on
    return result
