import os

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('APP_NAME'),
            'USER': os.environ.get('APP_NAME'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('MYSQL_DB_PORT_3306_TCP_ADDR'),
            'PORT': os.environ.get('MYSQL_DB_PORT_3306_TCP_PORT'),
            'TEST_CHARSET': 'utf8',
            'TEST_COLLATION': 'utf8_general_ci',
        }
    }

HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': "http://{0}:{1}".format(os.environ.get('ELASTIC_SEARCH_PORT_9200_TCP_ADDR'), os.environ.get('ELASTIC_SEARCH_PORT_9200_TCP_PORT')),
            'INDEX_NAME': os.environ.get('APP_NAME')
            }
        }