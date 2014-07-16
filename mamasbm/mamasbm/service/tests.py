import os
import transaction

from pyramid import testing
from unittest import TestCase
from webtest import TestApp

from mamasbm import main
from mamasbm.models import DBSession, Base, Profile
from mamasbm.web.csv_handler import CsvImporter
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

    def test_get_message(self):
        data = {'title': 'Mama basic', 'send_days': [1, 4]}
        resp = self.app.put_json('/web/api/profiles.json', data, status=200)
        sample_file = os.path.join(
            os.path.dirname(__file__), "../web/sample/english_pregnant.csv")

        resp = self.app.get('/web/api/profiles.json', status=200)
        profile_uuid = resp.json[0]['uuid'],
        factory.build_message_profiles('English', sample_file, profile_uuid)

        data = {'uuid': profile_uuid, 'day': 1, 'index': 0}
        resp = self.app.get('/api/message.json', data)
        self.assertTrue(resp.json['text'].startswith('Congrats on your pregnancy'))

        data = {'uuid': profile_uuid, 'day': 1, 'index': 5}
        resp = self.app.get('/api/message.json', data)
        self.assertTrue(resp.json['text'].startswith('Hello from MAMA. Most women start'))

        data = {'uuid': profile_uuid, 'day': 1, 'index': 35}
        resp = self.app.get('/api/message.json', data)
        self.assertTrue(resp.json['text'].startswith('Keep this SMS as your labour guide!'))

        data = {'uuid': profile_uuid, 'day': 4, 'index': 35}
        resp = self.app.get('/api/message.json', data)
        self.assertTrue(resp.json['text'].startswith('A tip from MAMA'))
