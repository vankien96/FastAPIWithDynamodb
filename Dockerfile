
ARG PYTHON_VERSION=3.11.5
FROM python:${PYTHON_VERSION}-slim as base

RUN mkdir -p /app

COPY requirements.txt /

RUN pip install -r /requirements.txt

# Copy the source code into the container.
COPY ./app /app

# Expose the port that the application listens on.
EXPOSE 8080

# Run the application.
CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port", "8080"]
