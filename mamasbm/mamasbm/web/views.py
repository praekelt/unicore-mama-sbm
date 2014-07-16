from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/home.pt')
def my_view(request):
    return {}


@view_config(route_name='admin', renderer='templates/admin.pt')
def admin(request):
    return {}


@view_config(route_name='admin_profiles', renderer='templates/profiles.pt')
def profiles_view(request):
    return {}


def not_found(request):
    return HTTPNotFound('Not found')
