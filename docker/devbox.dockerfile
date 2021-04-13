FROM python:3.9.4-buster

WORKDIR /app

ENV PYTHONPATH /app
ADD requirements.lock /app
RUN pip install --no-cache-dir -r requirements.lock

# Add the application source code.
ADD . /app

CMD bash