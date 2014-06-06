import transaction

from mamasbm import main
from pyramid import testing
from unittest import TestCase
from webtest import TestApp
from mamasbm.models import DBSession, Base, Profile


class TestProfilesView(TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.app = TestApp(main({}, **{'sqlalchemy.url': 'sqlite://'}))
        Base.metadata.create_all()

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_get_profiles_empty(self):
        resp = self.app.get('/web/api/profiles.json', status=200)
        self.assertEquals(len(resp.json['profiles']), 0)

    def test_get_profiles_success(self):
        with transaction.manager:
            model = Profile(
                title='Mama basic',
                send_days='1,4',
                num_messages_pre=36,
                num_messages_post=52
            )
            DBSession.add(model)
        resp = self.app.get('/web/api/profiles.json', status=200)
        self.assertEquals(len(resp.json['profiles']), 1)
        self.assertEquals(resp.json['profiles'][0]['title'], 'Mama basic')
