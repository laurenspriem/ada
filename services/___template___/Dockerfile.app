FROM python:3.9-slim

# Copy requirements
COPY requirements.txt /opt/service/requirements.txt

# Copy source code
COPY src /opt/service/src

# Install requirements
RUN pip install -r /opt/service/requirements.txt

# Set python path
ENV PYTHONPATH=/opt/service/src

# Set working directory
WORKDIR /opt/service

# Run server
ENV FLASK_ENV=development
ENV FLASK_APP=/opt/service/src/template/__main__.py

ENTRYPOINT ["flask", "run"]
CMD ["--host", "0.0.0.0", "--port", "8080"]
