'''
Created on Dec 6, 2017

@author: rpavlyuk
'''
from pyramid.view import view_config
from pyramid.response import Response

from pyramid.renderers import render_to_response


import logging
log = logging.getLogger(__name__)


'''
Processing file upload. All magic happens here!
'''
@view_config(route_name='upload_action', request_method='POST')
def upload_action(request):

    
    return Response("Uploaded")


'''
Rendering (presenting) the file upload form
'''
@view_config(route_name='upload_form', request_method='GET')
def upload_form(request):

    return render_to_response('templates/upload_form.pt',
                              {},
                              request=request)

'''
Handling index view. Basically, this is just a placeholder, nothing here is so far
'''
@view_config(route_name='index', request_method='GET')
def index(request):

    return Response("Index!")
    
    