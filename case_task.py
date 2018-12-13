#!/usr/bin/env python
# encoding: utf-8

from cortexutils.responder import Responder
import parse


def get_fields(self):
    # Retrieve the general information
    content = "Task details: \n"
    title = self.get_param('data.title', None, 'Title is missing')
    group = self.get_param('data.group', None, 'group is missing')
    status = self.get_param('data.status', None, 'status is missing')
    assignee = self.get_param('data.owner', None, 'assignee is missing')
    content = "Title: " + title + "\n"
    content = content + "Task group: " + group + "\n"
    content = content + "Status: " + status + "\n"  
    content = content + "Assignee: " + assignee + "\n"

    # Parse the description
    description = self.get_param('data.description', None, 'No description provided!')
    mail_chunks = parse.split_content(description)

    if len(mail_chunks['addresses']) == 0:
        self.error('recipient address not found in observables or content is missing!') 
    else: 
        # Build the email body
        mail_chunks['body'] = mail_chunks['body'] + content

    return mail_chunks
