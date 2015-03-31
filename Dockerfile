FROM aexea/aexea-base
MAINTAINER Stuttgart Python Interest Group

# install uwsgi for production
RUN pip3 install uwsgi

EXPOSE 8000

RUN mkdir -p /home/uid1000/feinstaub
RUN mkdir -p /home/uid1000/feinstaub/logs
RUN mkdir -p /home/uid1000/feinstaub/run
RUN chown -R uid1000: /home/uid1000

ADD requirements.txt /opt/code/requirements.txt
WORKDIR /opt/code
RUN pip3 install -Ur requirements.txt
ADD . /opt/code

RUN chown -R uid1000: /opt
RUN chmod 550 /opt/code/feinstaub/start.sh

WORKDIR feinstaub

# uid1000 is created in aexea-base
USER uid1000

# production stuff
CMD ["./start.sh"]
