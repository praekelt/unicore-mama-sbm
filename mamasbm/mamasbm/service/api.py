import transaction
from tempfile import NamedTemporaryFile

from cornice import Service
from sqlalchemy.exc import DBAPIError, StatementError

from mamasbm.models import DBSession, Profile
from mamasbm.service import validators


message = Service(
    name='message',
    path='/api/message.json',
    description="Public facing messages api"
)


@message.get(validators=validators.validate_get_message)
def get_message(request):
    uuid = request.validated['uuid']
    day = int(request.validated['day'])
    index = int(request.validated['index'])

    try:
        profile = DBSession.query(Profile).get(uuid)
        if not profile:
            request.errors.add('request', 'uuid', 'Profile not found.')
            return

        msg_profile = profile.message_profiles.filter_by(send_day=day).first()
        if not msg_profile:
            request.errors.add(
                'request', 'day',
                'This profile doesn\'t have messages for day %s.' % day)
            return

        messages = msg_profile.messages.order_by('week')
        num_messages = messages.count()
        if not num_messages:
            request.errors.add(
                'request', 'profile',
                'No messages available for this profile')
            return

        if index >= num_messages:
            request.errors.add('request', 'index', 'Index out of bounds')
            return

        return messages[index].to_dict()
    except DBAPIError:
        request.errors.add(
            'db', 'DBAPIError', 'Could not connect to the database.')
    except StatementError:
        request.errors.add('db', 'ValueError', 'uuid is not valid.')
