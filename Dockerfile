FROM python:3.6
MAINTAINER Opendata Stuttgart

ENV DEBIAN_FRONTEND noninteractive

# Install repository containing postgresql-client-9.5
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg main" >> /etc/apt/sources.list.d/postgresql.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get update && apt-get install -y \
	lib32z1-dev \
	libmemcached-dev \
	locales \
	postgresql-client-9.5 \
	postgresql-server-dev-all \
	sudo \
	ttf-dejavu-core \
	&& rm -rf /var/lib/apt/lists/*

RUN useradd uid1000 -d /home/uid1000 \
	&& mkdir -p /home/uid1000 \
	&& chown uid1000: /home/uid1000
VOLUME /home/uid1000

EXPOSE 8000

USER root

ADD requirements.txt /opt/code/requirements.txt
WORKDIR /opt/code
RUN pip3 install -Ur requirements.txt
ADD . /opt/code

RUN chown -R uid1000: /opt

WORKDIR /opt/code/feinstaub
USER root

# production stuff
ENTRYPOINT ["./start.sh"]
CMD ["web"]
