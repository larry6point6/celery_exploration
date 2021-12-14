# Experimenting with Celery

I need to create an api that will execute a long process, something along the lines of this asynchronously

```python
def long_process(a,b):
    sleep(1000)
    return a + b
```

It is expected the user will do something like:

```python
r = requests.post("http://endpoint/long_process" json={"a":1, "b":2})
```

and get back a job id, something like the below:

```python
r.json()
{"job_id": 2}
```

which will allow user to then do:

```python
r = requests.get("http://endpoint/long_process?job_id=2")
r.json()
{"result": 2}
or
{"result": None}
```

This is going to be containerised using docker compose, for the services required.

The docker compose yaml will contain three services/containers

1. The API
2. Celery worker
3. Redis

Once the environment is set up, next will be reading through the documentation on celery.
