import json
import transaction

from cornice import Service
from sqlalchemy.exc import DBAPIError

from mamasbm.models import DBSession, Profile

profiles = Service(
    name='profiles',
    path='/web/api/profiles.json',
    description="Manages stage based messaging profiles"
)


@profiles.get()
def get_profiles(request):
    try:
        all_profiles = DBSession.query(Profile).all()
        return {'profiles': [p.to_dict() for p in all_profiles]}
    except DBAPIError:
        request.errors.add('Could not connect to the database.')


def validate_required_field(request, name):
    data = json.loads(request.body)
    if name not in data or not data[name]:
        request.errors.add('body', name, '%s is a required field' % name)
    else:
        request.validated[name] = data[name]


def valid_put_request(request):
    validate_required_field(request, 'title')
    validate_required_field(request, 'send_days')
    validate_required_field(request, 'num_messages_pre')
    validate_required_field(request, 'num_messages_post')


@profiles.put(validators=valid_put_request)
def put_profiles(request):
    post_data = {
        'title': request.validated['title'],
        'send_days': request.validated['send_days'],
        'num_messages_pre': request.validated['num_messages_pre'],
        'num_messages_post': request.validated['num_messages_post']
    }
    try:
        with transaction.manager:
            model = Profile(**post_data)
            DBSession.add(model)
        return {'success': True}
    except DBAPIError:
        request.errors.add('Could not connect to the database.')
