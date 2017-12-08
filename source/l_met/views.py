'''
Created on Dec 6, 2017

@author: rpavlyuk
'''
from pyramid.view import view_config
from pyramid.response import Response
import pyramid.httpexceptions as exc

from pyramid.renderers import render_to_response

from l_met import util, db
import uuid, os, shutil


import logging
log = logging.getLogger(__name__)


'''
Processing file upload. All magic happens here!
'''
@view_config(route_name='upload_action', request_method='POST')
def upload_action(request):
    
    log.info("Received file upload request from %s" % request.remote_addr)
    
    # Check if the file is really being sent
    if 'image' not in request.POST:
        log.error("Missing PORT parameter 'image'")
        raise exc.HTTPBadRequest()
    if 'meter_id' not in request.POST:
        log.error("Missing PORT parameter 'meter_id'")
        raise exc.HTTPBadRequest()
    
    # Get application configuration
    config = util.get_config()

    # Get the filename
    filename = request.POST['image'].filename
    log.debug("Original filename: %s" % filename)
    
    # Get meter_id from POST request
    meter_id = request.POST['meter_id']
    log.debug("Received meter_id: %s" % meter_id)
    
    # Check if meter_id is not empty
    # NOTE: Empty string in Python are falsy so we check it like this:
    if not meter_id:
        log.error("Meter ID is empty!")
        raise exc.HTTPBadRequest()        
    
    # Get file contents
    input_file = request.POST['image'].file
    
    # Storing file in temporary location
    temp_file_path = os.path.join(config['storage']['cache'], '%s' % uuid.uuid4())
    log.debug("Temporary file: %s" % temp_file_path)
    
    # Finally write the data to a temporary file
    input_file.seek(0)
    with open(temp_file_path, 'wb') as output_file:
        shutil.copyfileobj(input_file, output_file)
        
    # let's check file if that the one we are looking for
    if not util.check_file(temp_file_path):
        log.error("File validation failed. Check the log file above for details.")
        raise exc.HTTPUnsupportedMediaType()
    else:
        log.info("File validation passed")
        
    # Now, after all validations, we can more the file to the storage
    file_store_path = os.path.join(config['storage']['store'], meter_id, '%s' % uuid.uuid4())
    log.debug("Moving image to the storage as %s" % file_store_path)
    # Creating subdirectory for meter_id if it doesn't exists
    directory = os.path.dirname(file_store_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    # moving the file to new directory
    shutil.move(temp_file_path, file_store_path)
    
    # Now, let's store file information in database
    db.put_file(meter_id, file_store_path)
    
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

    return Response("Index! It works!")

'''
Listing all available files
'''
@view_config(route_name='files_list', request_method='GET')
def files_list(request):

    return Response("Listing! It works!")
    