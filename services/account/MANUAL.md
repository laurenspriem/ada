# Service Template Manual

The template in this directory can be used to build microservices using [Flask](https://flask.palletsprojects.com/en/2.1.x/), [SQLAlchemy](https://www.sqlalchemy.org/) and [Google Pub/Sub](https://cloud.google.com/pubsub/docs/overview). The service can be deployed and tested using [Docker](https://docs.docker.com/) and [Docker Compose](https://docs.docker.com/compose/). The examples given in this manual are based on building an application that acts as a platform on which users can buy and sell second hand clothes.

## 1. Architecture

The service follows the [3-Tier Architecture Model](https://en.wikipedia.org/wiki/Multitier_architecture#Three-tier_architecture).

The resources layer is responsible for accepting incoming requests over `http(s)` or `pub/sub`. It converts the incoming data to python objects which can be used by the next layer. In the case of this template the resource layer is implemented by the `resources.py` and `tasks.py` files. The `resources.py` file handles all incoming `http(s)` requests (using [Flask](https://flask.palletsprojects.com/en/2.1.x/)). The `tasks.py` file handles the incoming messages of the topics that the service is subscribed to (using [Google Pub/Sub](https://cloud.google.com/pubsub/docs/overview)).

The interactions layer is the next layer in the [3-Tier Architecture Model](https://en.wikipedia.org/wiki/Multitier_architecture#Three-tier_architecture). This layer is responsible for implementing the business logic of the service. For example, when a user confirms another user's bid a few things need to happen: the item needs to be removed from the marketplace, a payment request needs to be made and the other user needs to receive a notification that its bid is accepted. Upon receiving this request the interactions layer needs to fulfill all these tasks and ensure the correct information is sent to the database, other services and Google Pub/Sub. To achieve the connections to these other systems and services it uses the repositories layer.

The repositories layer is the final layer in the [3-Tier Architecture Model](https://en.wikipedia.org/wiki/Multitier_architecture#Three-tier_architecture). This layer is responsible for implementing the logic to connect to databases, other services, Google Pub/Sub or Google Cloud Storage. This template already contains a few repositories to communicate with other services, these will be explained in the [Structure](#2-structure) section.

**Diagram**

```
incoming HTTP(s) Request
incoming Pub/Sub Message
            │
            │
  ┌─────────▼──────────┐
  │                    │
  │   Resources Layer  │
  │    resources.py    │
  │      tasks.py      │
  │                    │
  └─────────┬──────────┘
            │
            │
  ┌─────────▼──────────┐
  │                    │
  │ Interactions Layer │
  │  interactions.py   │
  │                    │
  └─────────┬──────────┘
            │
            │
  ┌─────────▼──────────┐
  │                    │
  │ Repositories Layer │
  │  repositories.py   │
  │                    │
  └────────────────────┘
```

## 2. Structure

The template contains a lot of different files this may seem daunting at first, however, only an understanding of a small subset of these files is required to build services using this template. The sections below contain an explanation for each file, and whether you should work in the file or not.

### 2.1 Files To Open

* `./src/template/app.py`: This file contains the main logic to start the [Flask](https://flask.palletsprojects.com/en/2.1.x/) application and Google Pub/Sub [Worker](https://huey.readthedocs.io/en/latest/index.html). Very few things need to be changed here, but you might want to remove or add repositories, to do this update the code in lines: `107-119` and `138-150`. This automagically makes the repositories available to the interactions layer under their specified key (i.e. `database_repository`).

* `./src/template/interactions.py`: This file contains the business logic for the service. All the logic should be organized in classes, preferably one class per data model (i.e. `BidInteractions` or `ItemInteractions`) but this is not a hard constraint. Each interactions class should take an `**repositories` parameter in its constructor, this parameter can be used as a dictionary to fetch repositories by the key you specified for the repository in the `app.py` file (i.e. `database_repository`). Then create functions in the class for each scenario you need to implement (i.e. `list()`, `store()`, `update()`, etc.).

* `./src/template/models.py`: This file contains the database models used in the service. [SQLAlchemy](https://www.sqlalchemy.org/) is used to implement these models. Furthermore, each model should implement a `to_dict()` function that converts the model to a dictionary (required for flask).

* `./src/template/repositories.py`: This file contains the logic to interact with the database, other services, Google Pub/Sub or Google Cloud Storage. It is again preferred to create a separate repository for each data model. However, the Pub/Sub and Web repositories are exceptions to this. To add additional topics to the Pub/Sub repository add them like the topic on line `23`. To add additional services to the Web repository add them like the service on line `90`. For creating new Database repositories just copy the `ExampleDatabaseRepository` class and update it where necessary.

* `./src/template/resources.py`: This file contains the code for handling incoming `http(s)` requests. If you need to import additional interactions copy the code on  line `11-12` and update it accordingly.

* `./src/template/tasks.py`: This file contains the code for handling incoming pub/sub messages. The current implementation is not an actual pub/sub implementation it uses a worker to check if there are new messages every minute. To create a new subscription copy the code on lines `11-13` and update it accordingly. Additionally you can change the interval at which the function checks for new messages by updating the [crontab](https://huey.readthedocs.io/en/latest/api.html#crontab) on line `11`. If you need to import additional interactions copy the code on  line `7-8` and update it accordingly.

* `./requirements.txt`: This file contains the requirements for the service. To add additional requirements append them to this file and then they will be automagically installed by docker.

### 2.2 Files To Ignore

* `./src/template/__init__.py`: Required for python to discover the files in this directory.

* `./src/template/__main__.py`: Used by the dockerfiles to run the `app` and `worker`.

* `./src/template/db.py`: Contains the [SQLAlchemy](https://www.sqlalchemy.org/) `Base` model.

* `./src/template/web.py`: Contains the `http(s)` client used to connect to other services.

* `./Dockerfile.app`: Contains the [Docker](https://docs.docker.com/) instructions for running the [Flask](https://flask.palletsprojects.com/en/2.1.x/) app.

* `./Dockerfile.worker`: Contains the [Docker](https://docs.docker.com/) instructions for running the [Worker](https://huey.readthedocs.io/en/latest/index.html) app.

## 3. How To Run/Test

The template is fully dockerized, this means that the only requirement to run the template is [Docker](https://docs.docker.com/). Each service had two Dockerfiles: `Dockerfile.app` runs the flask app and `Dockerfile.worker` runs the worker app for [Google Pub/Sub](https://cloud.google.com/pubsub/docs/overview). All the services are orchestrated using [Docker Compose](https://docs.docker.com/compose/). The `docker-compose.yml` file contains the instructions for [Docker](https://docs.docker.com/) to bring up every service and worker as well as a [PostgreSQL](https://www.postgresql.org/) database and an [Google Pub/Sub](https://cloud.google.com/pubsub/docs/overview) emulator.

The `env` section in the `docker-compose.yml` allows customization of the service using environment variables:

* `GOOGLE_APPLICATION_CREDENTIALS`: Path to the Google application credentials `*.json` file.

* `DB_HOST`: IP address or hostname of the database server.

* `DB_PORT`: Port of the database server usually `5432`.

* `DB_USER`: Username to connect to the database server.

* `DB_PASSWORD`: Password to connect to the database server.

* `DB_NAME`: Name of the database.

* `PUBSUB_EMULATOR_HOST`: Hostname and IP address of the pubsub emulator.

* `PUBSUB_PROJECT_ID`: Google Cloud project id.

The `volumes` section in the `docker-compose.yml` file mounts two files and directories in the container:

* `./google-application-credentials.json:/opt/gcloud/google-application-credentials.json`: The credentials for Google Cloud (NEVER COMMIT THIS FILE). In order for Docker to find this file, the `*.json` file should be in the root of the repository with filename: `google-application-credentials.json`.

* `./services/___template___/src:/opt/service/src`: The source code for the service, allows Flask to automatically reload when code is changed.

To startup the application run the following command: `docker-compose -p fintet -f docker-compose.yml up` in your terminal.

## 4. Converting Indika's Labs To Service Template

**Creating A New Service**

1. Copy the `___template___` folder and rename it to [YOUR_SERVICE_NAME].

2. In the `Dockerfile.app` file update line `20` with [YOUR_SERVICE_NAME].

3. In the `Dockerfile.worker` file update line `19` with [YOUR_SERVICE_NAME].

4. Rename the `template` directory the the `src` directory to [YOUR_SERVICE_NAME].

5. Update all the imports in the `src/[YOUR_SERVICE_NAME]` directory to reflect your new service name (i.e. `import template.resources` becomes `import [YOUR_SERVICE_NAME].resources`).

6. Implement the code for the specific tasks your service needs to perform.

7. Remove the code in the service that your not using.

8.  Add a new section to the `docker-compose.yml` file to add the service to the existing infrastructure:

```yml
[YOUR_SERVICE_NAME]_app:
  build:
    context: ./services/[YOUR_SERVICE_NAME]
    dockerfile: Dockerfile.app
  depends_on:
    - postgres
    - pubsub
  environment:
    - GOOGLE_APPLICATION_CREDENTIALS=/opt/gcloud/google-application-credentials.json
    - DB_HOST=postgres
    - DB_PORT=5432
    - DB_USER=postgres
    - DB_PASSWORD=postgres
    - DB_NAME=[YOUR_SERVICE_NAME]
    - PUBSUB_EMULATOR_HOST=pubsub:8085
    - PUBSUB_PROJECT_ID=jads-adaassignment
  volumes:
    - ./google-application-credentials.json:/opt/gcloud/google-application-credentials.json
    - ./services/[YOUR_SERVICE_NAME]/src:/opt/service/src

[YOUR_SERVICE_NAME]_worker:
  build:
    context: ./services/[YOUR_SERVICE_NAME]
    dockerfile: Dockerfile.worker
  depends_on:
    - postgres
    - pubsub
  environment:
    - GOOGLE_APPLICATION_CREDENTIALS=/opt/gcloud/google-application-credentials.json
    - DB_HOST=postgres
    - DB_PORT=5432
    - DB_USER=postgres
    - DB_PASSWORD=postgres
    - DB_NAME=template
    - PUBSUB_EMULATOR_HOST=pubsub:8085
    - PUBSUB_PROJECT_ID=jads-adaassignment
  volumes:
    - ./google-application-credentials.json:/opt/gcloud/google-application-credentials.json
    - ./services/[YOUR_SERVICE_NAME]/src:/opt/service/src
```

**Conveting An Existing Service**

1. All classes in the `daos` directory need to be moved to `models.py`. For each of the classes you need to remove the constructor (`def __init__(self, ...)`) and implement the `to_dict()` function.

2. All classes in the `resources` directory need to be moved to repositories. For each of the classes you can remove the `@staticmethod` decorators, use the `self._session` instead of creating a new session everytime (`session = Session()`) and return a plain Python object instead of using `jsonify()`.

3. Move all routes in `app.py` to `resources.py`. For each of the decorators rename the `app` decorator to `resources`. Instead of directly invoking the functions in the `resources` directory, invoke the functions in the `interactions` directory and from those invoke the `repositories`.
