'''
Created on Dec 6, 2017

@author: rpavlyuk
'''
from pyramid.view import view_config
from pyramid.response import Response

from pyramid.renderers import render_to_response


import logging
log = logging.getLogger(__name__)




@view_config(route_name='upload_form', request_method='GET')
def upload_form(request):
    return render_to_response('templates/upload_form.pt',
                              {'foo':1, 'bar':2},
                              request=request)


@view_config(route_name='index', request_method='GET')
def index(request):
    return Response("Index!")
    
    