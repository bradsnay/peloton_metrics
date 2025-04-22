FROM python:3.13

WORKDIR /app

ENV PYTHONPATH /app
ENV GOOGLE_APPLICATION_CREDENTIALS /app/secrets/pelotonmetrics-service-account.json

ADD requirements.lock /app
RUN pip install --no-cache-dir -r requirements.lock

RUN apt update && apt install -y --no-install-recommends odbc-postgresql

# Add the application source code.
ADD . /app

ENTRYPOINT python /app/peloton_metrics/run/run_workout_refresh.py