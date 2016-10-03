FROM python:2
MAINTAINER shaun@samsite.ca

# for dev/deploy
VOLUME /root/.aws

RUN pip install \
  awscli \
  pytz \
  boto3 \
  python-dateutil \
  lambda-uploader

ADD pocketlog /code

# tests will fail without aws creds and screw baking that shit in here
CMD cd /code/pocketlog && \
  python -m unittest discover pocketlog && \
  cd /code && \
  lambda-uploader -V ./pocketlog
