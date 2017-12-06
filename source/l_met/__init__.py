'''
Created on Dec 6, 2017

@author: rpavlyuk
'''
"""
Main entry point
"""
from pyramid.config import Configurator

from l_met import views


def main(global_config, **settings):
    config = Configurator(settings=settings)
    
    # routes
    config.add_route('index', '/')
    config.add_route('upload_form', '/upload/form')
    config.add_route('upload_action', '/upload/action')
    
    #views
    config.add_view(views.index, route_name='index')
    
    config.scan()
    
    config.include('pyramid_chameleon')
    
    return config.make_wsgi_app()