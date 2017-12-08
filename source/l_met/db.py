'''
Created on Dec 8, 2017

L-MET: Database methods and routines

@author: rpavlyuk
'''
import logging
log = logging.getLogger(__name__)

'''
Stores file information in the database
'''
def put_file(meter_id, file_path):
    
    log.info("Saving information for file " + file_path + " with meter_id " + meter_id + " to database")
    
    # TODO: Store file in the database; return record id
    
    return True
