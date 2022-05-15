# Function Template Manual

The template in this directory can be used to build [Google Cloud Functions](https://cloud.google.com/functions/docs) using [Functions Framework](https://cloud.google.com/functions/docs/functions-framework), [SQLAlchemy](https://www.sqlalchemy.org/) and [Google Pub/Sub](https://cloud.google.com/pubsub/docs/overview). The function can be tested using [Docker](https://docs.docker.com/) and [Docker Compose](https://docs.docker.com/compose/). The examples given in this manual are based on building an application that acts as a platform on which users can buy and sell second hand clothes.

## 1. Architecture

The function follows the [3-Tier Architecture Model](https://en.wikipedia.org/wiki/Multitier_architecture#Three-tier_architecture).

The resources layer is responsible for accepting incoming requests over `http(s)` or `pub/sub`. It converts the incoming data to python objects which can be used by the next layer. In the case of this template the resource layer is implemented by the `main.py` file. This file handles all incoming `http(s)` requests (using [Flask](https://flask.palletsprojects.com/en/2.1.x/)), as well as the incoming messages of the topics that the function is subscribed to (using [Google Pub/Sub](https://cloud.google.com/pubsub/docs/overview)).

The interactions layer is the next layer in the [3-Tier Architecture Model](https://en.wikipedia.org/wiki/Multitier_architecture#Three-tier_architecture). This layer is responsible for implementing the business logic of the function. For example, when a user confirms another user's bid a few things need to happen: the item needs to be removed from the marketplace, a payment request needs to be made and the other user needs to receive a notification that its bid is accepted. Upon receiving this request the interactions layer needs to fulfill all these tasks and ensure the correct information is sent to the database, other functions and Google Pub/Sub. To achieve the connections to these other systems and functions it uses the repositories layer.

The repositories layer is the final layer in the [3-Tier Architecture Model](https://en.wikipedia.org/wiki/Multitier_architecture#Three-tier_architecture). This layer is responsible for implementing the logic to connect to databases, other functions, Google Pub/Sub or Google Cloud Storage. This template already contains a few repositories to communicate with other functions, these will be explained in the [Structure](#2-structure) section.

**Diagram**

```
incoming HTTP(s) Request
incoming Pub/Sub Message
            │
            │
  ┌─────────▼──────────┐
  │                    │
  │   Resources Layer  │
  │       main.py      │
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

The template contains a lot of different files this may seem daunting at first, however, only an understanding of a small subset of these files is required to build functions using this template. The sections below contain an explanation for each file, and whether you should work in the file or not.

### 2.1 Files To Open

* `./main.py`: This file contains the main logic to start the function and implements the code for handling incomming `http(s)` requests or incomming pub/sub messages. Apart from the endpoints very few things need to be changed here, but you might want to remove or add repositories, to do this update the code in lines: `72`, `86` and `97`.

* `./interactions.py`: This file contains the business logic for the function. All the logic should be organized in classes, preferably one class per data model (i.e. `BidInteractions` or `ItemInteractions`) but this is not a hard constraint. Each interactions class should take its required repositories as parameters in its constructor. Then create functions in the class for each scenario you need to implement (i.e. `list()`, `store()`, `update()`, etc.).

* `./models.py`: This file contains the database models used in the function. [SQLAlchemy](https://www.sqlalchemy.org/) is used to implement these models. Furthermore, each model should implement a `to_dict()` function that converts the model to a dictionary (required for `json` conversion).

* `./repositories.py`: This file contains the logic to interact with the database, other functions, Google Pub/Sub or Google Cloud Storage. It is again preferred to create a separate repository for each data model. However, the Pub/Sub and Web repositories are exceptions to this. To add additional topics to the Pub/Sub repository add them like the topic on line `23`. To add additional functions to the Web repository add them like the function on line `90`. For creating new Database repositories just copy the `ExampleDatabaseRepository` class and update it where necessary.

* `./requirements.txt`: This file contains the requirements for the function. To add additional requirements append them to this file and then they will be automagically installed by docker.

### 2.2 Files To Ignore

* `./db.py`: Contains the [SQLAlchemy](https://www.sqlalchemy.org/) `Base` model.

* `./web.py`: Contains the `http(s)` client used to connect to other functions.

* `./Dockerfile`: Contains the [Docker](https://docs.docker.com/) instructions for running the [Google Cloud Function](https://cloud.google.com/functions/docs) using the [Functions Framework](https://cloud.google.com/functions/docs/functions-framework).

## 3. How To Run/Test

The template is fully dockerized, this means that the only requirement to run the template is [Docker](https://docs.docker.com/). All the functions are orchestrated using [Docker Compose](https://docs.docker.com/compose/). The `docker-compose.yml` file contains the instructions for [Docker](https://docs.docker.com/) to bring up every function as well as a [PostgreSQL](https://www.postgresql.org/) database and an [Google Pub/Sub](https://cloud.google.com/pubsub/docs/overview) emulator.

The `env` section in the `docker-compose.yml` allows customization of the function using environment variables:

* `GOOGLE_APPLICATION_CREDENTIALS`: Path to the Google application credentials `*.json` file.

* `DB_HOST`: IP address or hostname of the database server.

* `DB_PORT`: Port of the database server usually `5432`.

* `DB_USER`: Username to connect to the database server.

* `DB_PASSWORD`: Password to connect to the database server.

* `DB_NAME`: Name of the database.

* `FUNC_TARGET`: Name of the function in `main.py` you want to execute.

* `FUNC_SOURCE`: Path to `main.py` inside the container.

* `PUBSUB_EMULATOR_HOST`: Hostname and IP address of the pubsub emulator.

* `PUBSUB_PROJECT_ID`: Google Cloud project id.

The `volumes` section in the `docker-compose.yml` file mounts two files and directories in the container:

* `./google-application-credentials.json:/opt/gcloud/google-application-credentials.json`: The credentials for Google Cloud (NEVER COMMIT THIS FILE). In order for Docker to find this file, the `*.json` file should be in the root of the repository with filename: `google-application-credentials.json`.

* `./functions/___template___:/opt/function`: The source code for the function, allows functions framework to automatically reload when code is changed.

To startup the application run the following command: `docker-compose -p fintet -f docker-compose.yml up` in your terminal.

## 4. Converting Indika's Labs To Function Template

**Creating A New Function**

1. Copy the `___template___` folder and rename it to [YOUR_FUNCTION_DIRECTORY].

2. Implement the code for the specific tasks your function needs to perform.

3. Remove the code in the function that your not using.

4. For each function you want to execute add a new section to the `docker-compose.yml` file and update the `FUNC_TARGET` variable accordingly:

```yml
[YOUR_FUNCTION_TO_EXECUTE]_func:
    build:
      context: ./functions/[YOUR_FUNCTION_DIRECTORY]
      dockerfile: Dockerfile
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
      - FUNC_TARGET=[YOUR_FUNCTION_TO_EXECUTE]
      - FUNC_SOURCE=/opt/function/main.py
      - PUBSUB_EMULATOR_HOST=pubsub:8085
      - PUBSUB_PROJECT_ID=jads-adaassignment
    volumes:
      - ./google-application-credentials.json:/opt/gcloud/google-application-credentials.json
      - ./functions/[YOUR_FUNCTION_DIRECTORY]:/opt/function
```

**Conveting An Existing Service**

\-
