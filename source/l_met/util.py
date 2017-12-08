'''
Created on Dec 7, 2017

@author: rpavlyuk
'''

import magic

import logging
log = logging.getLogger(__name__)


'''
Returns configuration array
'''
def get_config():
    
    # creating configuration structure (dict type)
    config = dict(
        # file storage settings
        storage = dict(
            # where to store files
            store = '/var/www/sites/project/data/storage',
            #folder to temprorary cache files before storing them permanently
            cache = '/var/www/sites/project/data/cache'
            ),
        media = dict(
            # Supported image types
            supported_types = ('image/jpeg', 'image/png', 'image/bmp'),
            # Max width of the image
            max_width = 2048,
            # Max height of the image
            max_height = 1024,
            # Max file size (in bytes)
            max_size = 2048000
            )
        
        )
    
    return config;

'''
Check file's mime type
'''
def check_mime_type(file_path):
    
    # get the configuration
    config = get_config()
    
    # create Mime validation object
    mime = magic.Magic(mime=True)
    
    # now, check our file for its mime type
    mtype = mime.from_file(file_path)
    log.debug("Media type detected: %s" % mtype)
    
    if mtype not in config['media']['supported_types']:
        log.error("Unsupported MIME type: %s" % mtype)
        return False
    else:
        return True
    

'''
Check file size
'''
def check_file_size(file_path):
    
    # TODO: Add file size validation
    
    return True

'''
Check image size (width x height)
'''
def check_image_size(file_path):
    
    # TODO: Add image size (W x H) validation
    
    return True
        

'''
Check if file conforms the requirements:
 - is JPEG/PNG/BPM image
 - doesn't exceed the dimensions (TODO)
 - doesn't exceed the size (TODO)
'''
def check_file(file_path):
    
    # Checking mime type
    if not check_mime_type(file_path):
        return False
   
    # Checking file size
    if not check_file_size(file_path):
        return False
    
    # Check image dimensions
    if not check_image_size(file_path):
        return False   
        
    return True