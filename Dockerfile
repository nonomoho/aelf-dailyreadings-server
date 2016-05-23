FROM alpine:3.3
MAINTAINER Jean-Tiare Le Bigot <jt@yadutaf.fr>

RUN apk add --no-cache python py-lxml py-pip
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python2", "server.py"]
