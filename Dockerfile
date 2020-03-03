# choosing the img in this case its a lite version that
# runs python 3.7
FROM python:3.7-alpine
# the name of the maintainer
MAINTAINER ahmed mohamed

ENV PYTHONUNBUFFERED 1

# copy the local requirements.txt into the image dir
# and then install the requirements
copy ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

# making the work directory that all the apps on this img
# are gonna start from it
RUN mkdir /app
WORKDIR /app
copy ./app /app

# creating a user for the image for running apps only
Run adduser -D user
USER user