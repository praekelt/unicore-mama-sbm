import transaction

from cornice import Service
from sqlalchemy.exc import DBAPIError, StatementError

from mamasbm.models import DBSession, Profile
from mamasbm.web import validators


profiles = Service(
    name='profiles',
    path='/web/api/profiles.json',
    description="Manages stage based messaging profiles"
)


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
        request.errors.add(
            'db', 'DBAPIError', 'Could not connect to the database.')
    except StatementError:
        request.errors.add('db', 'ValueError', 'uuid is not valid.')


@profiles.put(validators=validators.validate_put_request)
def put_profiles(request):
    send_days = ', '.join(
        [str(x) for x in request.validated['send_days']])

    post_data = {
        'title': request.validated['title'],
        'send_days': send_days,
    }
    try:
        with transaction.manager:
            model = Profile(**post_data)
            DBSession.add(model)
        return {'success': True}
    except DBAPIError:
        request.errors.add('Could not connect to the database.')


@profiles.post(validators=validators.validate_post_request)
def post_profiles(request):
    uuid = request.validated['uuid']
    title = request.validated.get('title')
    send_days = request.validated.get('send_days')
    try:
        with transaction.manager:
            profile = DBSession.query(Profile).get(uuid)
            if title:
                profile.title = title
            if send_days:
                profile.send_days = ', '.join(
                    [str(x) for x in send_days])
            return profile.to_dict()
    except DBAPIError:
        request.errors.add('Could not connect to the database.')


@profiles.delete(validators=validators.validate_delete_request)
def delete_profile(request):
    uuid = request.validated['uuid']
    try:
        with transaction.manager:
            profile = DBSession.query(Profile).get(uuid)
            DBSession.delete(profile)
        return {'success': True}
    except DBAPIError:
        request.errors.add('Could not connect to the database.')
