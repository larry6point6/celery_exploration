import time

from celery import Celery

# implicit knowledge in that, it's not explicit
# Scenario base docker compose image,
# apply overrides, dev test they would override the base one
# docker compose up, docker compose down to clear everything up
# swagger documentation
# looking out for your iteration cycle, how quick it is
# always when you're developing
# ETL breakpoint


app = Celery("tasks", backend="redis://localhost", broker="redis://localhost")


@app.task
def add(x, y):
    return x + y
