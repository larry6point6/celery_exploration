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

Working through the API and realised that it would be quite nice to have a log file baked in so, created a log file and updated the celery command in the docker compose file. So instead of having to check the terminal, you can view what's happening in the log file.

80% of the way there can accomplish the task set out in a limited way, only via using the query string approach, attempting to use JSON presents an issue with function. My varying attempts are in the celery log.

To explore this project, you can use the following commands.

```docker-compose build``` in the root directory of the repo, to build the image.

```docker-compose up -d``` to spin up the containers in the background. Please note if the port 5000 is being used by anything else you will get a port already in use exception, easily solved if it's a docker container by stopping that container like so
```docker stop <container_id> (first few letters are fine)``` or cancelling whatever process is running using port 5000.

```docker-compose ps``` to check the containers have spun up correctly, can also look at the dashboard within Docker Desktop.

You can add a task to be sent to the celery worker like so on your device navigate to the below endpoint

```http://localhost:5000/add?a=3&b=4```

This will return something similar to this

```json
{
  "job_id": "6a0fdb54-910d-448b-84fd-3921c062efbc"
}
```

With the job_id, you can check the status of the job using the below endpoint,

```
http://localhost:5000/task/<job_id>
```

depending on the status of the job you will get back.

```json
{
    "result": null
    }
```

or

```json
{
  "result": 17
}
```

The next task was to enable the use of a debugger within the celery worker, this took some configuring and some trial and error to eventually get it working. All which is detailed in the branch test_rpdb branch of this repo.

In order to access your remote debugger all you need is the following command ```telnet localhost 4444```
and you should be presented with something like the below and be able to use the pdb. Remember to trigger the API by sending a task.

``` bash
> telnet localhost 4444
Trying ::1...
Connected to localhost.
Escape character is '^]'.
> /app/celery_app.py(18)add_task()
-> return result
(Pdb) 
```
