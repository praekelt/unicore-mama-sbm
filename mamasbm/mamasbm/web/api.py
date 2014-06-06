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
        return request.errors.add(
            'Pyramid is having a problem using your SQL database.')
