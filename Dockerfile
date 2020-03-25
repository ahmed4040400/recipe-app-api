# choosing the img in this case its a lite version that
# runs python 3.7
FROM python:3.7-alpine
# the name of the maintainer
MAINTAINER ahmed mohamed

ENV PYTHONUNBUFFERED 1

# copy the local requirements.txt into the image dir
# and then install the requirements
copy ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
# installing temp packages to be able install the postges
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN pip install -r requirements.txt

RUN apk del .tmp-build-deps

# making the work directory that all the apps on this img
# are gonna start from it
RUN mkdir /app
WORKDIR /app
copy ./app /app

# making the direictorys that's gonna handle the static and media files
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static


# creating a user for the image for running apps only
Run adduser -D user
# grnading a full permission to the user to controle the vol files
RUN chown -R user:user /vol/
RUN chown -R 755 /vol/web/
USER user