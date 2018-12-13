#!/usr/bin/env python
# encoding: utf-8

from cortexutils.responder import Responder
import parse


def get_fields(self):
    # Retrieve the general information
    content = "<p><b>Task details </b></p>"
    title = self.get_param('data.title', None, 'Title is missing')
    group = self.get_param('data.group', None, 'group is missing')
    status = self.get_param('data.status', None, 'status is missing')
    assignee = self.get_param('data.owner', None, 'assignee is missing')
    content = "<p><b> Title:</b> " + title + "<br>"
    content = content + "<b>Task group:</b> " + group + "<br>"
    content = content + "<b>Status:</b> " + status + "<br>"  
    content = content + "<b>Assignee:</b> " + assignee + "<br> </p>"

    # Parse the description
    description = self.get_param('data.description', None, 'No description provided!')
    mail_chunks = parse.split_content(description)

    if len(mail_chunks['addresses']) == 0:
        self.error('recipient address not found in observables or content is missing!') 
    else: 
        # Build the email body
        mail_chunks['body'] = mail_chunks['body'] + content

    return mail_chunks
