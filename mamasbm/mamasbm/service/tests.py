import os
import transaction
import uuid

from pyramid import testing
from unittest import TestCase
from webtest import TestApp

from mamasbm import main
from mamasbm.models import DBSession, Base, Profile, MessageProfile
from mamasbm.web import factory


class TestApi(TestCase):
    def setUp(self):
        self.config = testing.setUp()
        connection_string = os.environ.get(
            "MAMASBM_TEST_CONNECTION_STRING", "sqlite://")
        self.app = TestApp(main({}, **{'sqlalchemy.url': connection_string}))
        Base.metadata.create_all()

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()
        Base.metadata.drop_all()

    def test_get_profiles_db_error(self):
        # drop all the tables
        Base.metadata.drop_all()

        data = {'uuid': uuid.uuid4(), 'day': 1, 'index': 0}
        resp = self.app.get('/api/message.json', data, status=400)
        self.assertEquals(resp.json['status'], 'error')
        self.assertEquals(
            resp.json['errors'][0]['description'],
            'Could not connect to the database.'
        )

    def import_pregnancy_messages(self):
        data = {'title': 'Mama basic', 'send_days': [1, 4]}
        self.app.put_json('/web/api/profiles.json', data, status=200)
        sample_file = os.path.join(
            os.path.dirname(__file__), "../web/sample/english_pregnant.csv")

        resp = self.app.get('/web/api/profiles.json', status=200)
        profile_uuid = resp.json[0]['uuid'],
        factory.build_message_profiles(
            'English', sample_file, profile_uuid)
        return profile_uuid

    def test_get_message(self):
        profile_uuid = self.import_pregnancy_messages()

        data = {'uuid': profile_uuid, 'day': 1, 'index': 0}
        resp = self.app.get('/api/message.json', data)
        self.assertTrue(
            resp.json['text'].startswith('Congrats on your pregnancy'))

        data = {'uuid': profile_uuid, 'day': 1, 'index': 5}
        resp = self.app.get('/api/message.json', data)
        self.assertTrue(
            resp.json['text'].startswith('Hello from MAMA. Most women start'))

        data = {'uuid': profile_uuid, 'day': 1, 'index': 35}
        resp = self.app.get('/api/message.json', data)
        self.assertTrue(
            resp.json['text'].startswith('Keep this SMS as your labour guide'))

        data = {'uuid': profile_uuid, 'day': 4, 'index': 35}
        resp = self.app.get('/api/message.json', data)
        self.assertTrue(resp.json['text'].startswith('A tip from MAMA'))

    def test_error_messages(self):
        profile_uuid = self.import_pregnancy_messages()

        data = {'uuid': str(uuid.uuid4()), 'day': 1, 'index': 0}
        resp = self.app.get('/api/message.json', data, status=400)
        self.assertEqual(
            resp.json['errors'][0]['description'], 'Profile not found.')

        data = {'uuid': profile_uuid, 'day': 5, 'index': 0}
        resp = self.app.get('/api/message.json', data, status=400)
        self.assertEqual(
            resp.json['errors'][0]['description'],
            'This profile doesn\'t have messages for day 5.')

        data = {'uuid': profile_uuid, 'day': 1, 'index': 77}
        resp = self.app.get('/api/message.json', data, status=400)
        self.assertEqual(
            resp.json['errors'][0]['description'],
            'Index out of bounds')

        data = {'uuid': 'xxx', 'day': 1, 'index': 77}
        resp = self.app.get('/api/message.json', data, status=400)
        self.assertEqual(
            resp.json['errors'][0]['description'], 'uuid is not valid.')

        # create a blank profile
        data = {'title': 'Mama blank profile', 'send_days': [1, 2]}
        self.app.put_json('/web/api/profiles.json', data, status=200)
        resp = self.app.get('/web/api/profiles.json', status=200)
        profile_uuid = resp.json[1]['uuid']
        with transaction.manager:
            profile = DBSession.query(Profile).get(profile_uuid)
            msg_profile = MessageProfile(name='Blank - Tuesday')
            msg_profile.send_day = 1
            profile.message_profiles.append(msg_profile)

        data = {'uuid': profile_uuid, 'day': 1, 'index': 0}
        resp = self.app.get('/api/message.json', data, status=400)
        self.assertEqual(
            resp.json['errors'][0]['description'],
            'No messages available for this profile')

    def test_required_fields(self):
        resp = self.app.get('/api/message.json', status=400)
        self.assertEqual(
            resp.json['errors'][0]['description'],
            'uuid is a required field.')
        self.assertEqual(
            resp.json['errors'][1]['description'],
            'day is a required field.')
        self.assertEqual(
            resp.json['errors'][2]['description'],
            'index is a required field.')
