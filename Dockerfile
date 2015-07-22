FROM aexea/django-base
MAINTAINER Stuttgart Python Interest Group

EXPOSE 8000

USER root
RUN apt-get update && apt-get install -y ttf-dejavu-core
RUN easy_install3 -U pip

ADD requirements.txt /opt/code/requirements.txt
WORKDIR /opt/code
RUN pip3 install -Ur requirements.txt
ADD . /opt/code

RUN chown -R uid1000: /opt

WORKDIR feinstaub

# uid1000 is created in aexea-base
USER uid1000

# production stuff
CMD ["/bin/bash ./start.sh"]
