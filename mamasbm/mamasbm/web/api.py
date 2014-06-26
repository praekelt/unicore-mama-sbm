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


def update_validated_field(request, data, key):
    if key in data and data[key]:
        request.validated[key] = data[key]


def validate_required_field(request, data, key):
    if key not in data or not data[key]:
        request.errors.add('body', key, '%s is a required field.' % key)
    else:
        update_validated_field(request, data, key)


@profiles.get()
def get_profiles(request):
    uuid = request.GET.get('uuid', None)
    try:
        if uuid:
            profile = DBSession.query(Profile).get(uuid)
            if not profile:
                request.errors.add('Profile not found.')
                return
            return profile.to_dict()

        qs = DBSession.query(Profile).all()
        return [p.to_dict() for p in qs]
    except DBAPIError:
        request.errors.add('Could not connect to the database.')


def validate_put_request(request):
    data = json.loads(request.body)
    validate_required_field(request, data, 'title')
    validate_required_field(request, data, 'send_days')
    validate_required_field(request, data, 'num_messages_pre')
    validate_required_field(request, data, 'num_messages_post')


@profiles.put(validators=validate_put_request)
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


def validate_post_request(request):
    data = json.loads(request.body)
    validate_required_field(request, data, 'uuid')

    update_validated_field(request, data, 'title')
    update_validated_field(request, data, 'send_days')
    update_validated_field(request, data, 'num_messages_pre')
    update_validated_field(request, data, 'num_messages_post')


def validate_delete_request(request):
    data = json.loads(request.body)
    validate_required_field(request, data, 'uuid')


@profiles.post(validators=validate_post_request)
def post_profiles(request):
    uuid = request.validated['uuid']
    title = request.validated.get('title')
    send_days = request.validated.get('send_days')
    num_messages_pre = request.validated.get('num_messages_pre')
    num_messages_post = request.validated.get('num_messages_post')
    try:
        with transaction.manager:
            profile = DBSession.query(Profile).get(uuid)
            if title:
                profile.title = title
            if send_days:
                profile.send_days = send_days
            if num_messages_pre:
                profile.num_messages_pre = num_messages_pre
            if num_messages_post:
                profile.num_messages_post = num_messages_post
        return {'success': True}
    except DBAPIError:
        request.errors.add('Could not connect to the database.')


@profiles.delete(validators=validate_delete_request)
def delete_profile(request):
    uuid = request.validated['uuid']
    try:
        with transaction.manager:
            profile = DBSession.query(Profile).get(uuid)
            DBSession.delete(profile)
        return {'success': True}
    except DBAPIError:
        request.errors.add('Could not connect to the database.')
