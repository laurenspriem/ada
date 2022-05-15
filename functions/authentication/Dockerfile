FROM python:3.9-slim

# Copy requirements
COPY requirements.txt /opt/function/requirements.txt

# Copy source code
COPY . /opt/function

# Install requirements
RUN pip install -r /opt/function/requirements.txt

# Set working directory
WORKDIR /opt/function

# Run function
CMD functions-framework --target $FUNC_TARGET --source $FUNC_SOURCE --host 0.0.0.0 --port 8080 --debug
