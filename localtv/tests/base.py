# Miro Community - Easiest way to make a video website
#
# Copyright (C) 2009, 2010, 2011, 2012 Participatory Culture Foundation
#
# Miro Community is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# Miro Community is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Miro Community. If not, see <http://www.gnu.org/licenses/>.

import os
from datetime import datetime, timedelta
from socket import getaddrinfo

from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.template.defaultfilters import slugify
from django.test.testcases import TestCase, _deferredSkip
from django.test.client import RequestFactory
from haystack import connections
from tagging.models import Tag

from localtv.models import Video, Watch, Category
from localtv.middleware import UserIsAdminMiddleware

#: Global variable for storing whether the current global state believe that
#: it's connected to the internet.
HAVE_INTERNET_CONNECTION = None

class FakeRequestFactory(RequestFactory):
    """Constructs requests with any necessary attributes set."""
    def request(self, **request):
        request = super(FakeRequestFactory, self).request(**request)
        request.user = AnonymousUser()
        UserIsAdminMiddleware().process_request(request)
        SessionMiddleware().process_request(request)
        return request


class BaseTestCase(TestCase):
    def _clear_index(self):
        """Clears the search index."""
        backend = connections['default'].get_backend()
        backend.clear()

    def _update_index(self):
        """Updates the search index."""
        backend = connections['default'].get_backend()
        index = connections['default'].get_unified_index().get_index(Video)
        backend.update(index, index.index_queryset())

    def _rebuild_index(self):
        """Clears and then updates the search index."""
        self._clear_index()
        self._update_index()

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.factory = FakeRequestFactory()

    def create_video(self, name='Test.', status=Video.ACTIVE, site_id=1,
                     watches=0, categories=None, authors=None, tags=None,
                     update_index=True, **kwargs):
        """
        Factory method for creating videos. Supplies the following defaults:

        * name: 'Test'
        * status: :attr:`Video.ACTIVE`
        * site_id: 1

        In addition to kwargs for the video's fields, which are passed directly
        to :meth:`Video.objects.create`, takes a ``watches`` kwarg (defaults to
        0). If ``watches`` is greater than 0, that many :class:`.Watch`
        instances will be created, each successively one day further in the
        past.

        List of category and author instances may also be passed in as
        ``categories`` and ``authors``, respectively.

        """
        video = Video(name=name, status=status, site_id=site_id, **kwargs)
        video.save(update_index=update_index)

        for i in xrange(watches):
            self.create_watch(video, days=i)

        if categories is not None:
            video.categories.add(*categories)

        if authors is not None:
            video.authors.add(*authors)

        if tags is not None:
            video.tags = tags

        # Update the index here to be sure that the categories and authors get
        # indexed correctly.
        if status == Video.ACTIVE and site_id == 1:
            index = connections['default'].get_unified_index().get_index(Video)
            index._enqueue_update(video)
        return video

    def create_category(self, site_id=1, **kwargs):
        """
        Factory method for creating categories. Supplies the following
        default:

        * site_id: 1

        Additionally, ``slug`` will be auto-generated from ``name`` if not
        provided. All arguments given are passed directly to
        :meth:`Category.objects.create`.

        """
        if 'slug' not in kwargs:
            kwargs['slug'] = slugify(kwargs.get('name', ''))
        return Category.objects.create(site_id=site_id, **kwargs)

    def create_user(self, **kwargs):
        """
        Factory method for creating users. All arguments are passed directly
        to :meth:`User.objects.create`.

        """
        return User.objects.create(**kwargs)

    def create_tag(self, **kwargs):
        """
        Factory method for creating tags. All arguments are passed directly
        to :meth:`Tag.objects.create`.

        """
        return Tag.objects.create(**kwargs)

    def create_watch(self, video, ip_address='0.0.0.0', days=0):
        """
        Factory method for creating :class:`Watch` instances.

        :param video: The video for the :class:`Watch`.
        :param ip_address: An IP address for the watcher.
        :param days: Number of days to place the :class:`Watch` in the past.

        """
        watch = Watch.objects.create(video=video, ip_address=ip_address)
        watch.timestamp = datetime.now() - timedelta(days)
        watch.save()
        return watch

    def _data_file(self, filename):
        """
        Returns the absolute path to a file in our testdata directory.
        """
        return os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                'testdata',
                filename))

    def assertStatusCodeEquals(self, response, status_code):
        """
        Assert that the response has the given status code.  If not, give a
        useful error mesage.
        """
        self.assertEqual(response.status_code, status_code,
                          'Status Code: %i != %i\nData: %s' % (
                response.status_code, status_code,
                response.content or response.get('Location', '')))


def _have_internet_connection():
    global HAVE_INTERNET_CONNECTION

    if HAVE_INTERNET_CONNECTION is None:
        try:
            getaddrinfo("google.com", "http")
        except IOError:
            HAVE_INTERNET_CONNECTION = False
        else:
            HAVE_INTERNET_CONNECTION = True

    return HAVE_INTERNET_CONNECTION


def skipUnlessInternet():
    """
    Skip a test unless it seems like the machine running the test is
    connected to the internet.

    """
    return _deferredSkip(lambda: not _have_internet_connection(),
                         "Not connected to the internet.")
