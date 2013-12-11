# Mirocommunity
#
# VERSION   0.1
FROM ubuntu:12.10
MAINTAINER Filip Jukić <filip@appsembler.com>

RUN apt-get update
RUN apt-get install -y python-software-properties python-setuptools python-dev libxml2-dev libxslt-dev lib32z1-dev git-core nginx
RUN easy_install pip
RUN mkdir -p /opt/app
RUN cd /opt/app && pip install -e git+git://github.com/pculture/mirocommunity.git@1.10.0#egg=mirocommunity --no-deps
RUN pip install -r /opt/app/src/mirocommunity/test_project/requirements.txt
RUN pip install uwsgi supervisor
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
ADD .docker/miro.conf /etc/nginx/sites-enabled/miro.conf
ADD .docker/supervisord.conf /etc/supervisord.conf
RUN python /opt/app/src/mirocommunity/test_project/manage.py syncdb --noinput
ADD .docker/mkadmin.py /opt/app/src/mirocommunity/test_project/mkadmin.py
RUN cd /opt/app/src/mirocommunity/test_project && DJANGO_SETTINGS_MODULE=test_project.settings python mkadmin.py

EXPOSE 80
CMD ["supervisord", "-c", "/etc/supervisord.conf"]
