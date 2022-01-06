# Experimenting Remote Debugger

To explore this project, you can use the following commands.

```docker-compose build``` in the root directory of the repo, to build the images.

```docker-compose up -d``` to spin up the containers in the background. Please note if the port 5000 is being used by anything else you will get a port already in use exception, easily solved if it's a docker container by stopping that container like so

```docker stop <container_id> (first few letters are fine)``` or s

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

An additional task was to enable the worker to be debugged using Python's remote debugger, I've tried to get this working but still can't quite get the networking and the ports working correctly. This is what I've tried so far. I'll provide some screenshots and explanation of my thought process.

I started [here](https://pypi.org/project/rpdb/) at the pypi package pge for rpdb and followed the steps,
adding a breakpoint to the add function in ```celery_app.py``` by adding the following line
```import rpdb; rpdb.set_trace()```

When I attempt to call my task the logs are updated as follows

```
[2022-01-06 10:12:58,344: INFO/MainProcess] celery@worker ready.
[2022-01-06 10:13:39,537: INFO/MainProcess] Task celery_app.add_task[ef1cc849-9e10-4eb6-8620-60eef01c7d9f] received
[2022-01-06 10:13:54,548: WARNING/ForkPoolWorker-1] pdb is running on 127.0.0.1:4444
```

As expected the task is hanging at the point of my breakpoint, if I try to telnet here I expect an error because 127.0.0.1:4444 is local host and it can't be accessed in this way.

Next step was to amend local host to 0.0.0.0 in order to allow access by passing addr and port arguments to rpdb. Which gives us the following updates in the log

```
[2022-01-06 10:24:53,631: INFO/MainProcess] celery@worker ready.
[2022-01-06 10:25:31,853: INFO/MainProcess] Task celery_app.add_task[c14deab6-9ade-476f-aaff-fff6ab8615e3] received
[2022-01-06 10:25:46,872: WARNING/ForkPoolWorker-1] pdb is running on 0.0.0.0:4444
```

Attempting to telnet in gives the following error

```bash
telnet 0.0.0.0 4444
Trying 0.0.0.0...
telnet: connect to address 0.0.0.0: Connection refused
telnet: Unable to connect to remote host
```

Taking on the advice from Matt, I exposed the port 4444 in the dockerfile for the web container. Tried to connect to rpdb and got a similar error to the above

``` bash
telnet 0.0.0.0 4444
Trying 0.0.0.0...
telnet: connect to address 0.0.0.0: Connection refused
telnet: Unable to connect to remote host
```

Next was to map the port on the container in the docker compose, which seemed to move us forward beyond the error of being unable to connect, however as soon as I connect, the connection is closed by a foreign host

``` bash
telnet 0.0.0.0 4444
Trying 0.0.0.0...
Connected to 0.0.0.0.
Escape character is '^]'.
Connection closed by foreign host.
```
