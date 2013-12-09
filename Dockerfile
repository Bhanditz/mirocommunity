# Mirocommunity
#
# VERSION   0.1
FROM ubuntu:13.04
MAINTAINER Filip Jukić <filip@appsembler.com>

RUN apt-get update
RUN apt-get install python-software-properties python-setuptools python-dev libxml2-dev libxslt-dev lib32z1-dev
RUN easy_install pip
RUN mkdir -p /opt/app
RUN virtualenv /opt/venv && cd /opt/venv && source bin/activate
RUN cd /opt/app && pip install -e git+git://github.com/pculture/mirocommunity.git@1.10.0#egg=mirocommunity --no-deps
RUN pip install -r /opt/app/src/mirocommunity/test_project/requirements.txt
RUN python /opt/app/src/mirocommunity/test_project/manage.py syncdb --noinput

EXPOSE 8000
ENTRYPOINT python /opt/app/src/mirocommunity/test_project/manage.py runserver 0.0.0.0:8000
