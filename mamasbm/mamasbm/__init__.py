from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from mamasbm.web import views
from mamasbm.models import (
    DBSession,
    Base,
)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.include("cornice")
    config.add_static_view('static', 'static')
    config.add_route('home', '/')
    config.add_route('admin', '/admin/')
    config.add_route('admin_profiles', '/admin/profiles/')
    config.add_notfound_view(views.not_found, append_slash=True)
    config.scan("mamasbm.service.api")
    config.scan("mamasbm.web.api")
    config.scan("mamasbm.web.views")
    return config.make_wsgi_app()
