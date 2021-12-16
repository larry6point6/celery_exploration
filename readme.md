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

After wrangling with the environment set up for a little while, I'm now able to get into the structure of the project.

Will start by testing that all the services behave as expected. I'm going to use Flask to accomplish this project and will use redis as both the message broker and cache for the messages.

After some guidance on my iteration cycle, I was able to spend some time understanding celery and workers and what I'm trying to achieve, I did this initially all in my local environment working through the documentation and using the REPL to rapidly test my approach. Working fine in my local environment but not quite working within Docker, got some ideas for what's causing the issue.

Now to tie this all together and create an API, that meets the original task.
