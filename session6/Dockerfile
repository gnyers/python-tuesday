FROM python:3-alpine
LABEL version="1.0" \
      license=GPLv2 \
      maintainer="Gábor Nyers"
LABEL description="A demo Python application to serve meta-data and user-data \
to cloud-init containers."
LABEL documentation="Start your container with: \
  docker run -d -p 5001:5001 cloud-init-data"

RUN apk update
RUN apk upgrade python-pip


COPY requirements.txt /tmp/
RUN \
    pip install -r /tmp/requirements.txt

COPY app/ /tmp/app/
ENV PYTHONPATH=/tmp \
    BIND_PORT=5001
EXPOSE 

CMD [ "python", "-m", "app" ]
