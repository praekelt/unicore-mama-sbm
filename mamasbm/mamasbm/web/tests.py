import os
import transaction
from StringIO import StringIO

from mamasbm import main
from pyramid import testing
from unittest import TestCase
from webtest import TestApp
from mamasbm.models import DBSession, Base, Profile
from mamasbm.web.csv_handler import CsvImporter
from mamasbm.web import factory


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
        self.assertEquals(len(resp.json), 0)

    def test_get_profiles_success(self):
        with transaction.manager:
            model = Profile(
                title='Mama basic',
                send_days='1, 4',
            )
            DBSession.add(model)
        resp = self.app.get('/web/api/profiles.json', status=200)
        self.assertEquals(len(resp.json), 1)
        self.assertEquals(resp.json[0]['title'], 'Mama basic')

    def test_put_profiles_success(self):
        payload = {
            'title': 'Mama basic',
            'send_days': [1, 4],
        }
        resp = self.app.put_json('/web/api/profiles.json', payload, status=200)
        self.assertTrue(resp.json['success'])

        resp = self.app.get('/web/api/profiles.json', status=200)
        self.assertEquals(len(resp.json), 1)
        self.assertEquals(resp.json[0]['title'], 'Mama basic')

    def test_get_profile_by_uuid(self):
        payload = {
            'title': 'Mama basic',
            'send_days': [1, 4],
        }
        resp = self.app.put_json('/web/api/profiles.json', payload, status=200)
        self.assertTrue(resp.json['success'])

        resp = self.app.get('/web/api/profiles.json', status=200)
        data = {'uuid': resp.json[0]['uuid']}

        resp = self.app.get('/web/api/profiles.json', data, status=200)
        self.assertEquals(resp.json['title'], 'Mama basic')

        resp = self.app.get(
            '/web/api/profiles.json?uuid=%(uuid)s' % data, status=200)
        self.assertEquals(resp.json['title'], 'Mama basic')

    def test_get_profile_by_uuid_invalid(self):
        payload = {
            'title': 'Mama basic',
            'send_days': '1,4',
        }
        resp = self.app.put_json('/web/api/profiles.json', payload, status=200)
        self.assertTrue(resp.json['success'])

        data = {'uuid': 'some-invalid-uuid'}
        resp = self.app.get('/web/api/profiles.json', data, status=400)
        self.assertEquals(
            resp.json['errors'][0]['description'],
            'uuid is not valid.')

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

        resp = self.app.get('/web/api/profiles.json', status=200)
        self.assertEquals(len(resp.json), 0)

    def test_put_profiles_title_missing_required_field(self):
        payload = {
            'send_days': '1,4',
        }
        resp = self.app.put_json('/web/api/profiles.json', payload, status=400)
        self.assertEquals(resp.json['status'], 'error')

        self.assertEquals(
            resp.json['errors'][0]['description'],
            'title is a required field.'
        )
        self.assertEquals(len(resp.json['errors']), 1)

        resp = self.app.get('/web/api/profiles.json', status=200)
        self.assertEquals(len(resp.json), 0)

    def test_update_profile_title(self):
        data = {
            'title': 'Mama basic',
            'send_days': [1, 4],
        }
        resp = self.app.put_json('/web/api/profiles.json', data, status=200)
        self.assertTrue(resp.json['success'])

        resp = self.app.get('/web/api/profiles.json', status=200)
        self.assertEquals(len(resp.json), 1)
        self.assertEquals(resp.json[0]['title'], 'Mama basic')
        data = {
            'title': 'Mama basic new',
            'uuid': resp.json[0]['uuid']
        }

        resp = self.app.post_json('/web/api/profiles.json', data, status=200)

        resp = self.app.get('/web/api/profiles.json', status=200)
        self.assertEquals(len(resp.json), 1)
        self.assertEquals(resp.json[0]['title'], 'Mama basic new')

    def test_update_profile_all(self):
        data = {
            'title': 'Mama basic',
            'send_days': [1, 4],
        }
        resp = self.app.put_json('/web/api/profiles.json', data, status=200)
        self.assertTrue(resp.json['success'])

        resp = self.app.get('/web/api/profiles.json', status=200)
        self.assertEquals(len(resp.json), 1)
        self.assertEquals(resp.json[0]['title'], 'Mama basic')
        data = {
            'title': 'Mama basic new',
            'send_days': [1, 7],
            'uuid': resp.json[0]['uuid']
        }

        resp = self.app.post_json('/web/api/profiles.json', data, status=200)

        resp = self.app.get('/web/api/profiles.json', status=200)
        self.assertEquals(len(resp.json), 1)
        self.assertEquals(resp.json[0]['title'], 'Mama basic new')
        self.assertEquals(resp.json[0]['send_days'], [1, 7])

    def test_delete_profile(self):
        data = {
            'title': 'Mama basic',
            'send_days': [1, 4],
        }
        resp = self.app.put_json('/web/api/profiles.json', data, status=200)
        self.assertTrue(resp.json['success'])

        resp = self.app.get('/web/api/profiles.json', status=200)
        self.assertEquals(len(resp.json), 1)
        self.assertEquals(resp.json[0]['title'], 'Mama basic')
        data = {
            'uuid': resp.json[0]['uuid']
        }

        resp = self.app.delete(
            '/web/api/profiles.json?uuid=%(uuid)s' % data, status=200)
        self.assertTrue(resp.json['success'])

        resp = self.app.get('/web/api/profiles.json', status=200)
        self.assertEquals(len(resp.json), 0)

    def test_get_profiles_db_error(self):
        # drop all the tables
        Base.metadata.drop_all()

        resp = self.app.get('/web/api/profiles.json', status=400)
        self.assertEquals(resp.json['status'], 'error')
        self.assertEquals(
            resp.json['errors'][0]['description'],
            'Could not connect to the database.'
        )

    def test_message_profile_csv_import(self):
        importer = CsvImporter(2)
        sample_file = os.path.join(
            os.path.dirname(__file__), "sample/english_pregnant.csv")
        days = importer.import_csv(sample_file)
        self.assertEquals(len(days.items()), 2)
        self.assertEquals(len(days[0].items()), 36)
        self.assertEquals(len(days[1].items()), 36)

    def test_message_profile_factory(self):
        data = {
            'title': 'Mama basic',
            'send_days': [1, 4],
        }
        resp = self.app.put_json('/web/api/profiles.json', data, status=200)
        self.assertTrue(resp.json['success'])

        resp = self.app.get('/web/api/profiles.json', status=200)
        self.assertEquals(len(resp.json), 1)
        self.assertEquals(resp.json[0]['title'], 'Mama basic')
        sample_file = os.path.join(
            os.path.dirname(__file__), "sample/english_pregnant.csv")

        profile_uuid = resp.json[0]['uuid'],
        factory.build_message_profiles('English', sample_file, profile_uuid)

        resp = self.app.get('/web/api/profiles.json', status=200)
        self.assertEquals(len(resp.json), 1)
        self.assertEquals(resp.json[0]['title'], 'Mama basic')
        self.assertEquals(resp.json[0]['send_days'], [1, 4])
        self.assertEquals(
            resp.json[0]['message_profiles'][0]['name'],
            'English - Monday')
        self.assertEquals(
            len(resp.json[0]['message_profiles'][0]['messages']),
            36)

    def test_delete_message_profile(self):
        data = {
            'title': 'Mama basic',
            'send_days': [1, 4],
        }
        resp = self.app.put_json('/web/api/profiles.json', data, status=200)
        self.assertTrue(resp.json['success'])

        sample_file = os.path.join(
            os.path.dirname(__file__), "sample/english_pregnant.csv")

        resp = self.app.get('/web/api/profiles.json', status=200)
        profile_uuid = resp.json[0]['uuid'],
        factory.build_message_profiles('English', sample_file, profile_uuid)

        resp = self.app.get('/web/api/profiles.json', status=200)
        self.assertEquals(len(resp.json), 1)
        self.assertEquals(resp.json[0]['title'], 'Mama basic')
        self.assertEquals(len(resp.json[0]['message_profiles']), 2)

        data = {
            'uuid': resp.json[0]['message_profiles'][0]['uuid'],
        }

        resp = self.app.delete(
            '/web/api/message_profiles.json?uuid=%(uuid)s' % data, status=200)
        self.assertTrue(resp.json['success'])

        resp = self.app.get('/web/api/profiles.json', status=200)
        self.assertEquals(len(resp.json[0]['message_profiles']), 1)
