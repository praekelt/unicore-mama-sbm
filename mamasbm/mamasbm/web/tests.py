from mamasbm import main
from pyramid import testing
from unittest import TestCase
from webtest import TestApp
from mamasbm.models import DBSession


class TestProfilesView(TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.app = TestApp(main({}, **{'sqlalchemy.url': 'sqlite://'}))

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_get_profiles(self):
        resp = self.app.get('/web/api/profiles.json', status=200)
        self.assertEquals(len(resp.json['profiles']), 2)
        self.assertEquals(resp.json['profiles'][0], 'profile1')
        self.assertEquals(resp.json['profiles'][1], 'profile2')
