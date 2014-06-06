from cornice import Service
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
)


@view_config(route_name='home', renderer='templates/home.pt')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(
            'Pyramid is having a problem using your SQL database.',
            content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'mamasbm'}

profiles = Service(
    name='profiles',
    path='/profiles.json',
    description="Manages stage based messaging profiles"
)


@profiles.get()
def get_profiles(request):
    return {'profiles': ['profile1', 'profile2']}
