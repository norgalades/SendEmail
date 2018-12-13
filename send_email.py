#!/usr/bin/env python
# encoding: utf-8

from cortexutils.responder import Responder
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from enum import Enum
import re
import case_task
import case_task_log

class Mailer(Responder):

    severity_dict = {1: "LOW", 2: "MEDIUM", 3: "HIGH"}

    def __init__(self):
        Responder.__init__(self)
        self.smtp_host = self.get_param(
            'config.smtp_host', 'localhost')
        self.mail_from = self.get_param(
            'config.from', None, 'Missing sender email address')
    
    def case_header(self):
        content = ""
	title = self.get_param('data.title', None, 'title is missing')
        description = self.get_param('data.description', None, 'description is missing')    	
        severity = self.get_param('data.severity', None, 'severity is missing')
	status = self.get_param('data.status', None, 'status is missing')
	owner = self.get_param('data.owner', None, 'owner is missing')
	content = title + "\n"
	content = content + "Description: " + description + "\n"  
	content = content + "Severity: " + Mailer.severity_dict[severity] + "\n"
	content = content + "Status: " + status + "\n"  
	content = content + "Owner: " + owner + "\n"
        return content

    def run(self):
        Responder.run(self)

	mail_to = None
        
	if self.data_type == 'thehive:case':
            title = self.get_param('data.title', None, 'title is missing')
            # Search recipient address in tags
            tags = self.get_param('data.tags', None, 'recipient address not found in tags')
            mail_tags = [t[5:] for t in tags if t.startswith('mail:')]
            if mail_tags:
                mail_to = mail_tags.pop()
            else:
                self.error('recipient address not found among tags')
	    # Build the email body
	    content = "Case: " 
            header = self.case_header()
	    content = content + header      

        elif self.data_type == 'thehive:case_task':
	    # Parse the task
            fields = case_task.get_fields(self)     
	
	elif self.data_type == 'thehive:case_task_log':
	    # Parse the log 
	    fields = case_task_log.get_fields(self)
	    	    	
        else:
            self.error('Invalid dataType')

        msg = MIMEMultipart()
        msg['Subject'] = fields['subject']
        msg['From'] = self.mail_from
        msg['To'] = ', '.join(fields['addresses'])
        msg.attach(MIMEText(fields['body'], 'plain'))

        s = smtplib.SMTP(self.smtp_host)
        s.sendmail(self.mail_from, fields['addresses'], msg.as_string())
        s.quit()
        self.report({'message': 'message sent'})

    def operations(self, raw):
        return [self.build_operation('AddTagToCase', tag='mail sent')]


if __name__ == '__main__':
    Mailer().run()
