FROM python:3.13

WORKDIR /app

ENV PYTHONPATH /app
ENV GOOGLE_APPLICATION_CREDENTIALS /app/secrets/pelotonmetrics-service-account.json

ADD requirements.lock /app
RUN pip install --no-cache-dir -r requirements.lock

# Update package lists and install dependencies
RUN apt update && apt install -y --no-install-recommends odbc-postgresql postgresql-client

# Add the application source code.
ADD . /app

CMD bash