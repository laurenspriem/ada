# ADA
[![License](https://img.shields.io/github/license/tomdewildt/ada)](https://github.com/tomdewildt/ada/blob/master/LICENSE)

Used for groupwork for the Advanced Data Architectures course at the JADS.

# How To Run

Prerequisites:
* docker version ```20.10.8``` or later
* docker-compose version ```1.27.4``` or later
* functions-framework version ```3.0.0``` or later
* make version ```4.2.1``` or later (optional)

### App

1. Run ```docker-compose -p fintet -f docker-compose.yml build``` or ```make build/app``` to build the containers (optional).
2. Run ```docker-compose -p fintet -f docker-compose.yml up``` or ```make run/app``` to start the containers.

Run ```make init``` to install the requirements of each service on your local machine (optional).

### Infrastructure

1. Run ```make stack/create name=[NAME] file=[FILE].yml``` to create a stack.
1. Run ```make stack/update name=[NAME] file=[FILE].yml``` to update a stack.

Run ```make stack/list``` to list all stacks and ```make stack/delete name=[NAME]``` to delete a stack.

# References

[Python Docs](https://docs.python.org/3/)

[Google Cloud Docs](https://cloud.google.com/docs)

[Compute Engine Docs](https://cloud.google.com/compute/docs)

[Cloud Functions Docs](https://cloud.google.com/functions/docs)

[Deployment Manager Docs](https://cloud.google.com/deployment-manager/docs)

[Docker Docs](https://docs.docker.com/)

[Dockerfile Docs](https://docs.docker.com/engine/reference/builder/)

[Docker Compose Docs](https://docs.docker.com/compose/)

[Black Formatter Docs](https://black.readthedocs.io/en/stable/)

[Pylint Linter Docs](https://pylint.pycqa.org/en/latest/)

[Flask Web Framework Docs](https://flask.palletsprojects.com/en/2.0.x/)

[Flask SQLAlchemy Docs](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)

[SQLAlchemy Database ORM Docs](https://docs.sqlalchemy.org/en/14/)

[Requests Web Client Docs](https://docs.python-requests.org/en/latest/)
