FROM python:3.7-alpine
LABEL maintainer="Tomasz Naskręt <tomasz.naskret@pwr.edu.pl>"

RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers

WORKDIR /app
COPY ./app .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -e .

RUN apk del .tmp-build-deps
