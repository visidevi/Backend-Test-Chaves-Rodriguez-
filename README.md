## cornershop-backend-test

### Running the development environment

- `make up`

```

dev migrate

```

```

python manage.py createsuperuser

username = nora

password = admin

```

If you use another user consider changing the variables in the postman environment that is attached with this repository

![Postman]('https://imgur.com/ESvP6vo')

```

dev up

```

## Development environment

A postman collection is available for testing.

[collection](./postman/Backend_Test.postman_collection.json)

[environment](./NORA-TOKEN.postman_environment.json)

The postman file has a pre_script that obtains the Nora token for authentication

### Create a Menu

Create menu with today's date

**POST:** `{{url}}/api/menus/`

**Request_body:**

```

{

"message": "Menu 19/02",

"date": "2022-02-19"

}

```

**Response**:

```

{

"id": "a9d46cda-4304-4616-8dff-24c41d874c4d",

"message": "Menu 19/02",

"date": "2022-02-19"

}

```

### Create options for the menu

**POST:**`{{url}}/api/menus/:pk/set-option/`

> {{url}}/api/menus/a9d46cda-4304-4616-8dff-24c41d874c4d/set-option/

**Args:**

`pk`: Pk of the menu to which you want to create the option

**Request_body:**

```

{

"description": "Curry de lentejas"

}

```

**Response:**

```

{

"id": 1,

"description": "Curry de lentejas",

"menu": "a9d46cda-4304-4616-8dff-24c41d874c4d"

}

```

### Slack Integration

Replace the `SLACK APP TOKEN` variables with your application's in the `backend_test/settings.py` file.

> `APP_TZ` = getenv("APP_TZ", default="America/Santiago") # Chile Timezone

`MAX_ORDER_HOUR` = getenv("MAX_ORDER_HOUR", default="11") # Maximum time allowed to create an order

`NOTIFICATION_HOUR` = getenv("NOTIFICATION_HOUR", default="10") # Time to send notifications to users

`SLACK_APP_TOKEN` = getenv("SLACK_APP_TOKEN", default=" ")

![Variables]('https://imgur.com/EAtB6Av')

### Celery

Raise an instance of celery beat

`docker ps`

Copy the container id from the image `cornershop-backend-test_backend`

```

docker container exec -it {container_id} /bin/bash

cd backend-test/

celery -A backend_test beat --loglevel DEBUG

```

![Celery Beat](https://imgur.com/WX73aui)

### Interact with user response

To be able to interact with the user from Slack we must enter `Request URL` in the configuration of our app in Slack

`https://api.slack.com/apps/XXXXID_APP_SLACK/interactive-messages?`

In local environments We can use `ngrok http 8000` to get a valid URL for Slack

> ngrok allows us to expose a dynamically generated URL to the internet, which points to a web service running on our local machine

![Request URL](https://imgur.com/H1juiJC)

![ngrok](https://imgur.com/DuWMydE)

#### DEMO

[![Demo](https://imgur.com/6TbYzXE)(https://www.youtube.com/watch?v=Csy5LnbmJQA&ab_channel=visakadevi)]

### Validations

-We cannot create two equal options to the same menu

-The User cannot create two orders on the same day

-The User cannot create orders after 11 Am

-Only Nora can create menus and options

-Notification will only be sent to users who are on Nora's channel and have a timezone in Chile

-The notification is sent at 10 Am \*\* Modifiable

### Test

```

python manage.py test

```

![Notification](https://imgur.com/BZO6vuO)

![Created Order](https://imgur.com/x8RJjZi)

![Customized Order](https://imgur.com/zpWxi7P)

![Validation](https://imgur.com/sWfpwUb)

![Validation](https://imgur.com/8jHQ7mq)

#### Coverage

`coverage run --source="." manage.py test`

`coverage report html`

##### Rebuilding the base Docker image

- `make rebuild`

##### Resetting the local database

- `make reset`

### Hostnames for accessing the service directly

- Local: http://127.0.0.1:8000

### About building local environment with Linux systems

If you bring up the local environment in a linux system, maybe you can get some problems about users permissions when working with Docker.

So we give you a little procedure to avoid problems with users permissions structure in Linux.:

1- Delete containers

```

# or docker rm -f $(docker ps -aq) if you don't use docker beyond the test

make down

```

2- Give permissions to your system users to use Docker

```

## Where ${USER} is your current user

sudo usermod -aG docker ${USER}

```

3- Confirm current user is in docker group

```

## If you don't see docker in the list, then you possibly need to log off and log in again in your computer.

id -nG

```

4- Get the current user id

```

## Commonly your user id number is near to 1000

id -u

```

5- Replace user id in Dockerfiles by your current user id

Edit `.docker/Dockerfile_base` and replace 1337 by your user id.

6- Rebuild the local environment

```

make rebuild

make up

```

### Celery beat local

docker container exec -it {id_contenedor} /bin/bash

cd backend-test/

```

celery -A backend_test beat --loglevel DEBUG

```

### Fixtures

`python manage.py dumpdata --format=json auth.user > fixtures/users.json`

`-format=json --pks 1 menus.menu > fixtures/menus.json`

`--format=json --pks 1 menus.option >> fixtures/options.json`
# Backend-Test-Chaves-Rodriguez-
