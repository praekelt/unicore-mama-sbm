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

    def test_put_profiles_success(self):
        payload = {
            'title': 'Mama basic',
            'send_days': '1,4',
            'num_messages_pre': 36,
            'num_messages_post': 52
        }
        resp = self.app.put_json('/web/api/profiles.json', payload, status=200)
        self.assertTrue(resp.json['success'])

        resp = self.app.get('/web/api/profiles.json', status=200)
        self.assertEquals(len(resp.json['profiles']), 1)
        self.assertEquals(resp.json['profiles'][0]['title'], 'Mama basic')

    def test_put_profiles_missing_required_fields(self):
        resp = self.app.put_json('/web/api/profiles.json', {}, status=400)
        self.assertEquals(resp.json['status'], 'error')

        self.assertEquals(
            resp.json['errors'][0]['description'],
            'title is a required field.'
        )
        self.assertEquals(
            resp.json['errors'][1]['description'],
            'send_days is a required field.'
        )
        self.assertEquals(
            resp.json['errors'][2]['description'],
            'num_messages_pre is a required field.'
        )
        self.assertEquals(
            resp.json['errors'][3]['description'],
            'num_messages_post is a required field.'
        )

        resp = self.app.get('/web/api/profiles.json', status=200)
        self.assertEquals(len(resp.json['profiles']), 0)

    def test_put_profiles_title_missing_required_field(self):
        payload = {
            'send_days': '1,4',
            'num_messages_pre': 36,
            'num_messages_post': 52
        }
        resp = self.app.put_json('/web/api/profiles.json', payload, status=400)
        self.assertEquals(resp.json['status'], 'error')

        self.assertEquals(
            resp.json['errors'][0]['description'],
            'title is a required field.'
        )
        self.assertEquals(len(resp.json['errors']), 1)

        resp = self.app.get('/web/api/profiles.json', status=200)
        self.assertEquals(len(resp.json['profiles']), 0)

    def test_update_profile_title(self):
        data = {
            'title': 'Mama basic',
            'send_days': '1,4',
            'num_messages_pre': 36,
            'num_messages_post': 52
        }
        resp = self.app.put_json('/web/api/profiles.json', data, status=200)
        self.assertTrue(resp.json['success'])

        resp = self.app.get('/web/api/profiles.json', status=200)
        self.assertEquals(len(resp.json['profiles']), 1)
        self.assertEquals(resp.json['profiles'][0]['title'], 'Mama basic')
        data = {
            'title': 'Mama basic new',
            'uuid': resp.json['profiles'][0]['uuid']
        }

        resp = self.app.post_json('/web/api/profiles.json', data, status=200)
        self.assertTrue(resp.json['success'])

        resp = self.app.get('/web/api/profiles.json', status=200)
        self.assertEquals(len(resp.json['profiles']), 1)
        self.assertEquals(resp.json['profiles'][0]['title'], 'Mama basic new')

    def test_update_profile_all(self):
        data = {
            'title': 'Mama basic',
            'send_days': '1,4',
            'num_messages_pre': 36,
            'num_messages_post': 52
        }
        resp = self.app.put_json('/web/api/profiles.json', data, status=200)
        self.assertTrue(resp.json['success'])

        resp = self.app.get('/web/api/profiles.json', status=200)
        self.assertEquals(len(resp.json['profiles']), 1)
        self.assertEquals(resp.json['profiles'][0]['title'], 'Mama basic')
        data = {
            'title': 'Mama basic new',
            'send_days': '1, 7',
            'num_messages_pre': 36,
            'num_messages_post': 60,
            'uuid': resp.json['profiles'][0]['uuid']
        }

        resp = self.app.post_json('/web/api/profiles.json', data, status=200)
        self.assertTrue(resp.json['success'])

        resp = self.app.get('/web/api/profiles.json', status=200)
        self.assertEquals(len(resp.json['profiles']), 1)
        self.assertEquals(resp.json['profiles'][0]['title'], 'Mama basic new')
        self.assertEquals(resp.json['profiles'][0]['send_days'], '1, 7')
        self.assertEquals(resp.json['profiles'][0]['num_messages_pre'], 36)
        self.assertEquals(resp.json['profiles'][0]['num_messages_post'], 60)

    def test_get_profiles_db_error(self):
        # drop all the tables
        Base.metadata.drop_all()

        resp = self.app.get('/web/api/profiles.json', status=400)
        self.assertEquals(resp.json['status'], 'error')
        self.assertEquals(
            resp.json['errors'][0]['location'],
            'Could not connect to the database.'
        )
