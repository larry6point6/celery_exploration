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

An additional task was to enable the worker to be debugged using Python's remote debugger, I've tried to get this working but still can't quite get the networking and the ports working correctly. This is what I've tried so far. I'll provide some snippets and explanation of my thought process.

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

Next was to map the port on the container in the docker compose, which seemed to move us forward beyond the error of being unable to connect, however as soon as I connect, the connection is closed immediately by a foreign host, I think it's something in the networking but I can't quite pin it down

``` bash
telnet 0.0.0.0 4444
Trying 0.0.0.0...
Connected to 0.0.0.0.
Escape character is '^]'.
Connection closed by foreign host.
```

After asking Matt for some help we started to break down the problem from different levels, starting with the network in order to do this

We went into the container and launched a shell using this command ```docker exec -it <container_name>``` can be accessed either by it's name or id can be found using ```docker ps```. We did a simple check that everything was working in the container we were able to access our debugger as expected. In order to achieve this we needed to install netcat within the docker container, this meant granting root access to our user in the docker container we did this by commenting out the config in the Dockerfile.

This suggested it might be a network error, something to do with either how I configured the docker compose or maybe something happening in the dockerfile for the web container.

Following the initial pattern we tried exposing port 4444 in the dockerfile, this didn't work. Matt then pointed out that in the docker-compose file I had the placed the ports in the wrong service, this was spotted following a docker ps and seeing which ports were mapped where, this was a simple fix of just moving the ports 4444:4444 to the worker service.

There were still some issues with netcat, however telnet seemed to work.

So in order for us to remotely access our debugger we need to use the following command ```telnet localhost 4444```, doing so will present you with a debugger in your terminal, remember to hit your endpoint to ensure that the debugger has something to connect to.

When we invoke local host, we are sending the packet back into yourself, whereas listening on port 0.0.0.0 is listen to everything, reject all connections unless they have come from the container itself, this needs a deeper dive, find something to help clarify this.

Using ```telnet localhost 4444``` will present you with a debugger allowing us to step through what is happening in our code.

This is a bit of a niche example you would probably start with built in debuggers but there are instances where this approach would be useful such as trying to debug multiple threads, instead of an interactive terminal it's a network terminal. Generally to be used as a last resort when particular circumstances call for it.
