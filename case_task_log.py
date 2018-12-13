#!/usr/bin/env python
# encoding: utf-8

from cortexutils.responder import Responder
import parse

def log_header(self):
	startdate = self.get_param('data.startDate', None, 'date is missing')
	status = self.get_param('data.status', None, 'log status is missing')
        if status == "Deleted":
	    return self.error('log has been deleted') 
	else:    
	    return startdate

def get_fields(self):
    # Retrieve log content
    log = self.get_param('data.message', None, 'No content found in this log!')
    # Search recipient address in the log content 
    mail_chunks = parse.split_content(log)

    if len(mail_chunks['addresses']) == 0:
        self.error('Recipient address not found! Check your log format.') 
    
    return mail_chunks     
