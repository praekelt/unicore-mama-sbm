from datetime import date

from cornice import Service
from sqlalchemy.exc import DBAPIError, StatementError

from mamasbm.models import DBSession, Profile
from mamasbm.service import validators


message = Service(
    name='message',
    path='/api/message.json',
    description="Public facing messages api"
)


#helper method to allow testing (mockable)
def get_ref_date():
    return date.today()


def get_message_counter(index, date, max_weeks):
    if index:
        return int(index)

    today = get_ref_date()

    prenatal = True if today < date else False
    print today, date, prenatal, max_weeks, (date - today).days / 7, (max_weeks - 1) - ((today - date).days / 7)
    if prenatal:
        return (date - today).days / 7
    return (max_weeks - 1) - ((today - date).days / 7)


@message.get(validators=validators.validate_get_message)
def get_message(request):
    uuid = request.validated['uuid']
    day = int(request.validated['day'])

    index = request.validated.get('index')
    date = request.validated.get('date')

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

        msg_counter = get_message_counter(index, date, num_messages)
        if msg_counter >= num_messages or msg_counter < 0:
            request.errors.add('request', 'index', 'Index out of bounds')
            return

        return messages[msg_counter].to_dict()
    except DBAPIError:
        request.errors.add(
            'db', 'DBAPIError', 'Could not connect to the database.')
    except StatementError:
        request.errors.add('db', 'ValueError', 'uuid is not valid.')
