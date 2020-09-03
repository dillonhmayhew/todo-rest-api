# React.js front-end UI

[Click](https://github.com/dillonhmayhew/react-flask-rest) here to see the front-end I built using [React.js](https://reactjs.org/)!

![Home](https://github.com/dillonhmayhew/todo-rest-api/blob/master/home.gif)

# todo-rest-api

This is a simple RESTful CRUD todo API built using Flask and SQLAlchemy. This is an almagamtion of various ideas from multiple sources and tutorials. The client can create a user profile and assign themselves tasks. All user and task data is stored in an SQLite database file named `app.db`. Users may clone this repository and use a local instance of this database for testing and playing around with.

[Installation](https://github.com/dillonhmayhew/todo-rest-api#installation)

[Detailed Examples](https://github.com/dillonhmayhew/todo-rest-api#play-time)

## Resources

The API gathers from two resources:

* **Users**
* **Tasks**

### Users

The **users** resource will use HTTP methods as follows:

HTTP Method | URI | Action
----------- | --- | ------
GET | http://[hostname]/api/users | Retrieve list of users
GET | http://[hostname]/api/users/[username] | Retrieve user
POST | http://[hostname]/api/users | Create a new user
PUT | http://[hostname]/api/users/[username] | Update an existing user
DELETE | http://[hostname]/api/users/[username] | Delete user

We can define a user as having the following fields:

* **id**: unique identifier for users. INTEGER.
* **username**: unique username for users. VARCHAR.
* **email**: unique email address for users. VARCHAR.
* **password_hash**: encrypted password. VARCHAR.

### Tasks

The **tasks** resource will use HTTP methods as follows:

HTTP Method | URI | Action
----------- | --- | ------
GET | http://[hostname]/api/tasks | Retrieve list of tasks
GET | http://[hostname]/api/tasks/[task_id] | Retrieve a task
POST | http://[hostname]/api/tasks | Create a new task
PUT | http://[hostname]/api/tasks/[task_id] | Update an existing task
DELETE | http://[hostname]/api/tasks/[task_id] | Delete a task

We can define a task as having the following fields:

* **id**: unique identifier for tasks. INTEGER.
* **title**: short task description. VARCHAR.
* **done**: task completion state. TINYINT.
* **description**: long task description. VARCHAR.
* **user_id**: *foreign key ref user.id*. INTEGER.

The `user_id` field is a *foreign key* that links the task to its owner. I have defined a *one-to-many* relationship between the `users` and `tasks` tables as shown in this schema created using the [WWW SQL Designer](http://ondras.zarovi.cz/sql/demo) tool:

![Image of schema](https://github.com/dillonhmayhew/todo-rest-api/blob/master/schema.png)

## Authorizaton

To secure this RESTful web service, I decided to use [Miguel Grinberg](https://blog.miguelgrinberg.com)'s Flask extension [Flask-HTTPAuth](https://github.com/miguelgrinberg/flask-httpauth). This limits accessibility to only registered users of the web service.

To add another layer of security, registered users have the option to generate a temporary authorization token by accessing the route `/api/token` with their login credentials. This token is generated using [PyJWT](https://github.com/jpadilla/pyjwt) and has a set expiry timeout. This prevents the need for a user to send their password over HTTP on every request and instead send a token that will be useless after it expires.

# Installation

[Python 3.5+](https://www.python.org/downloads/) must be installed on your system, as well as `pip`.

This code is using Python [3.7.3](https://www.python.org/downloads/release/python-373/)


**Clone the repository:**

`>git clone https://github.com/dillonhmayhew/todo-rest-api.git`

**Use Python 3's built in virtual environment package:** `python3 -m [module-name] [name of virtual environment]`

`>python3 -m venv flask`

**Note:** If you are using Ubuntu/Debian, you may have to install this as a separate distro package:

`>sudo apt-get install python3-venv`

`>python3 -m venv flask`

**Activating you're new virtual environment:**

On **Linux:**

`>. flask/bin/activate` **OR**

On **Windows:**

`>flask\Scripts\activate`

**Install the requirements of the application:**

`(flask) >pip install -r requirements.txt`

**Simply run the application:**

`(flask) >flask run`

# Play Time

Since web browsers cannot easily generate all types of HTTP requests, I will be using [curl](http://curl.haxx.se/). Many systems have `curl` pre-installed anyway, and I recommend using Git Bash over a regular CMD window if you are on windows. If you decide to use CMD you will have to do some escaping to nest double quotes.

## Users

### Creating a User

Let's create a user with the username `name`, email `name@example.com` and password `passwd`: 

```bat
$ curl -i -H "Content-Type: application/json" -X POST -d '{"username":"name", "email":"name@example.com", "passwd":"passwd"}' http://127.0.0.1:5000/api/users
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 146
Server: Werkzeug/1.0.1 Python/3.7.3
Date: Fri, 21 Aug 2020 18:51:55 GMT

{
  "user": {
    "tasks": 0,
    "uri": "http://127.0.0.1:5000/api/users/name",
    "username": "name",
    "email": "name@example.com"
  }
}
```

### Reading Users

Now that we have created a user, you may use these credentials as authorization throughout the API:

```bat
$ curl -u name:passwd -i http://127.0.0.1:5000/api/users
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 623
Server: Werkzeug/1.0.1 Python/3.7.3
Date: Fri, 21 Aug 2020 19:19:02 GMT

{
  "users": [
    {
      "tasks": 4,
      "uri": "http://127.0.0.1:5000/api/users/dillon",
      "username": "dillon",
      "email": "dillon@example.com"
    },
    {
      "tasks": 1,
      "uri": "http://127.0.0.1:5000/api/users/tyler",
      "username": "tyler",
      "email": "tyler@example.com"
    },
    {
      "tasks": 1,
      "uri": "http://127.0.0.1:5000/api/users/sandy",
      "username": "sandy",
      "email": "sandy@example.com"
    },
    {
      "tasks": 0,
      "uri": "http://127.0.0.1:5000/api/users/name",
      "username": "name",
      "email": "name@example.com"
    }
  ]
}
```

### Updating User

A user may only update their own information. When attempting to update the email of another user, you will be prompted by a 401 error code:

```bat
$ curl -u name:passwd -i -H "Content-Type: application/json" -X PUT -d '{"email":"change@example.com"}' http://127.0.0.1:5000/api/users/dillon
HTTP/1.0 401 UNAUTHORIZED
Content-Type: application/json
Content-Length: 37
Server: Werkzeug/1.0.1 Python/3.7.3
Date: Fri, 21 Aug 2020 19:27:01 GMT

{
  "error": "Unauthorized Access"
}
```
A global user variable is set when the credentials sent through the request are authenticated. If the user you are trying to update is not the authenticated user, the API will not allow this action to take place:

Let's update the email of name to `change@example.com`:

```bat
$ curl -u name:passwd -i -H "Content-Type: application/json" -X PUT -d '{"email":"change@example.com"}' http://127.0.0.1:5000/api/users/name
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 148
Server: Werkzeug/1.0.1 Python/3.7.3
Date: Fri, 21 Aug 2020 19:34:45 GMT

{
  "user": {
    "tasks": 0,
    "uri": "http://127.0.0.1:5000/api/users/name",
    "username": "name",
    "email": "change@example.com"
  }
}
```

### Deleting User

Similarly, a user may only delete themselves:

```bat
$ curl -u name:passwd -i -X DELETE http://127.0.0.1:5000/api/users/name
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 21
Server: Werkzeug/1.0.1 Python/3.7.3
Date: Fri, 21 Aug 2020 19:41:30 GMT

{
  "result": true
}
```

## Tasks

### Creating a Task

A task is by default considered not done, so you may enter a `title` and a `description` in a `POST` request:

```bat
$ curl -u dillon:mypassword -i -H "Content-Type: application/json" -X POST -d '{"title":"Create a task", "description":"a task to demonstrate creating a task"}' http://127.0.0.1:5000/api/tasks
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 179
Server: Werkzeug/1.0.1 Python/3.7.3
Date: Fri, 21 Aug 2020 19:51:48 GMT

{
  "task": {
    "uri": "http://127.0.0.1:5000/api/tasks/7",
    "title": "Create a task",
    "done": false,
    "description": "a task to demonstrate creating a task"
  }
}
```

### Reading Tasks

Let's look at my todo list:

```bat
$ curl -u dillon:mypassword -i http://127.0.0.1:5000/api/tasks
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 954
Server: Werkzeug/1.0.1 Python/3.7.3
Date: Fri, 21 Aug 2020 19:52:38 GMT

{
  "tasks": [
    {
      "uri": "http://127.0.0.1:5000/api/tasks/1",
      "title": "Create a RESTful todo api",
      "done": true,
      "description": "Flask, SLQAlchemy, SQLite, JSON."
    },
    {
      "uri": "http://127.0.0.1:5000/api/tasks/3",
      "title": "Read a book",
      "done": false,
      "description": "just kidding I cannot read"
    },
    {
      "uri": "http://127.0.0.1:5000/api/tasks/4",
      "title": "Blueprint todo api",
      "done": true,
      "description": "make use of flask blueprints to make application scalable"
    },
    {
      "uri": "http://127.0.0.1:5000/api/tasks/6",
      "title": "Improve GET tasks",
      "done": false,
      "description": "Configure GET tasks to take optional arguments"
    },
    {
      "uri": "http://127.0.0.1:5000/api/tasks/7",
      "title": "Create a task",
      "done": false,
      "description": "a task to demonstrate creating a task"
    }
  ]
}
```

As you can see, the newly created task appears along with it's unique URI.

### Updating Tasks

I have implemented `GET` tasks to take an optional argument of `done`. This will filter the results to show only the tasks that are either completed or incompleted.

Let's take a look at my completed tasks:

```bat
$ curl -u dillon:mypassword -i http://127.0.0.1:5000/api/tasks?done=1
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 411
Server: Werkzeug/1.0.1 Python/3.7.3
Date: Fri, 21 Aug 2020 20:07:54 GMT

{
  "tasks": [
    {
      "uri": "http://127.0.0.1:5000/api/tasks/1",
      "title": "Create a RESTful todo api",
      "done": true,
      "description": "Flask, SLQAlchemy, SQLite, JSON."
    },
    {
      "uri": "http://127.0.0.1:5000/api/tasks/4",
      "title": "Blueprint todo api",
      "done": true,
      "description": "make use of flask blueprints to make application scalable"
    }
  ]
}
```

Now we will update my task that is identified by `task_id` `6` to completed:

```bat
$ curl -u dillon:mypassword -i -H "Content-Type: application/json" -X PUT -d '{"done":true}' http://127.0.0.1:5000/api/tasks/6
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 191
Server: Werkzeug/1.0.1 Python/3.7.3
Date: Fri, 21 Aug 2020 19:55:39 GMT

{
  "task": {
    "uri": "http://127.0.0.1:5000/api/tasks/6",
    "title": "Improve GET tasks",
    "done": true,
    "description": "Configure GET tasks to take optional arguments"
  }
}
```

And once again, let's check to see my updated task list:

```bat
$ curl -u dillon:mypassword -i http://127.0.0.1:5000/api/tasks?done=1
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 604
Server: Werkzeug/1.0.1 Python/3.7.3
Date: Fri, 21 Aug 2020 20:10:04 GMT

{
  "tasks": [
    {
      "uri": "http://127.0.0.1:5000/api/tasks/1",
      "title": "Create a RESTful todo api",
      "done": true,
      "description": "Flask, SLQAlchemy, SQLite, JSON."
    },
    {
      "uri": "http://127.0.0.1:5000/api/tasks/4",
      "title": "Blueprint todo api",
      "done": true,
      "description": "make use of flask blueprints to make application scalable"
    },
    {
      "uri": "http://127.0.0.1:5000/api/tasks/6",
      "title": "Improve GET tasks",
      "done": true,
      "description": "Configure GET tasks to take optional arguments"
    }
  ]
}

```

### Deleting Tasks

We will go ahead and delete the example task I created earlier that is identified by `task_id` `7`:

```bat
$ curl -u dillon:mypassword -i -X DELETE http://127.0.0.1:5000/api/tasks/7
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 21
Server: Werkzeug/1.0.1 Python/3.7.3
Date: Fri, 21 Aug 2020 20:12:24 GMT

{
  "result": true
}
```

And now let's view my task list once again:

```bat
$ curl -u dillon:mypassword -i http://127.0.0.1:5000/api/tasks
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 772
Server: Werkzeug/1.0.1 Python/3.7.3
Date: Fri, 21 Aug 2020 20:14:29 GMT

{
  "tasks": [
    {
      "uri": "http://127.0.0.1:5000/api/tasks/1",
      "title": "Create a RESTful todo api",
      "done": true,
      "description": "Flask, SLQAlchemy, SQLite, JSON."
    },
    {
      "uri": "http://127.0.0.1:5000/api/tasks/3",
      "title": "Read a book",
      "done": false,
      "description": "just kidding I cannot read"
    },
    {
      "uri": "http://127.0.0.1:5000/api/tasks/4",
      "title": "Blueprint todo api",
      "done": true,
      "description": "make use of flask blueprints to make application scalable"
    },
    {
      "uri": "http://127.0.0.1:5000/api/tasks/6",
      "title": "Improve GET tasks",
      "done": true,
      "description": "Configure GET tasks to take optional arguments"
    }
  ]
}
```

## Generating a Token

To generate a temporary auth token, let's navigate to `/api/token` with my user credentials:

```bat
$ curl -u dillon:mypassword -i http://127.0.0.1:5000/api/token
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 163
Server: Werkzeug/1.0.1 Python/3.7.3
Date: Fri, 21 Aug 2020 20:16:00 GMT

{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNTk4MDQxNTYwLjY4MjI5MTd9.4PyCU2usxfP5O7dq7Dh5Pcj1Ix9w9fOv9J_N9amIXtA",
  "duration": 600
}
```

This token may now be used instead of a username and password:

```bat
$ curl -u eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNTk4MDQxNTYwLjY4MjI5MTd9.4PyCU2usxfP5O7dq7Dh5Pcj1Ix9w9fOv9J_N9amIXtA:irrelevant -i http://127.0.0.1:5000/api/tasks
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 772
Server: Werkzeug/1.0.1 Python/3.7.3
Date: Fri, 21 Aug 2020 20:18:36 GMT

{
  "tasks": [
    {
      "uri": "http://127.0.0.1:5000/api/tasks/1",
      "title": "Create a RESTful todo api",
      "done": true,
      "description": "Flask, SLQAlchemy, SQLite, JSON."
    },
    {
      "uri": "http://127.0.0.1:5000/api/tasks/3",
      "title": "Read a book",
      "done": false,
      "description": "just kidding I cannot read"
    },
    {
      "uri": "http://127.0.0.1:5000/api/tasks/4",
      "title": "Blueprint todo api",
      "done": true,
      "description": "make use of flask blueprints to make application scalable"
    },
    {
      "uri": "http://127.0.0.1:5000/api/tasks/6",
      "title": "Improve GET tasks",
      "done": true,
      "description": "Configure GET tasks to take optional arguments"
    }
  ]
}
```

As you can see, the token is authenticated to my user credentials. For the next 10 minutes I may use this token for all my CRUD needs.

A quick note that `...` `J_N9amIXtA:irrelevant` "irrelevant" can be anything, as there is no need for a password when using a token.
