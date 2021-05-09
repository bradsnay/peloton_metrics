FROM python:3.9.4-buster

WORKDIR /app

ENV PYTHONPATH /app
ENV GOOGLE_APPLICATION_CREDENTIALS /app/user_configs/pelotonmetrics-service-account.json

ADD requirements.lock /app
RUN pip install --no-cache-dir -r requirements.lock

# Add the application source code.
ADD . /app

CMD bash