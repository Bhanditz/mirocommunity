# Mirocommunity
#
# VERSION   0.1
FROM ubuntu:12.10
MAINTAINER Filip Jukić <filip@appsembler.com>

RUN apt-get update
RUN apt-get install -y python-software-properties python-setuptools python-dev libxml2-dev libxslt-dev lib32z1-dev git-core
RUN easy_install pip
RUN mkdir -p /opt/app
RUN cd /opt/app && pip install -e git+git://github.com/pculture/mirocommunity.git@1.10.0#egg=mirocommunity --no-deps
RUN pip install -r /opt/app/src/mirocommunity/test_project/requirements.txt
RUN python /opt/app/src/mirocommunity/test_project/manage.py syncdb --noinput
RUN pip install uwsgi

EXPOSE 80
CMD cd /opt/app/src/mirocommunity/test_project && uwsgi --chdir=/opt/app/src/mirocommunity/test_project --module=test_project.wsgi:application --env DJANGO_SETTINGS_MODULE=test_project.settings --master --pidfile=/tmp/project-master.pid --http :80 --processes=5 --harakiri=20 --limit-as=192 --max-requests=2000 --vacuum --static-map /static=/opt/app/src/mirocommunity/localtv/static
