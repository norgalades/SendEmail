#!/usr/bin/env python
# encoding: utf-8
import re


def split_content(content):
    chunks = {'addresses': [], 'subject': "", 'body': ""}
    # Parser can be equal to 'mailto', 'subject' or  'body'
    parser = ""

    for line in content.splitlines():
	# print("line: " + line)
	if "mailto:" in line: 
	    parser = "mailto"
	elif "subject:" in line:
	    parser = "subject"
	elif "body:" in line:
	    parser = "body"
	elif not line: 
	    continue

	if parser == "mailto":
	    # print("mailto")  
	    # Split the content to take the email addresses but the last which contains the message
            addresses = re.split("mailto:", line.strip())
            # Build the list and discard the first empty chunk
	    if len(addresses) == 2:
                addresses = re.split("; ", addresses[1])
	    else: 
                addresses = re.split("; ", addresses[0])
	    for i in addresses:
		# print("email: " + i)
		# print(chunks['addresses'])
                chunks['addresses'].append(i.strip())
	elif parser == "subject":
	    # print("Subject")
            # Parse the subject
            subject = re.split("subject:", line.strip())
	    if len(subject) == 2:
	        chunks['subject'] = chunks['subject'] + subject[1] + " " 
	    else: 
		chunks['subject'] = chunks['subject'] + subject[0] + " "
        elif parser == "body":
	    # print("body")
            # Parse the body
	    body = re.split("body:", line.strip())
	    if len(body) == 2:
	        chunks['body'] = chunks['body'] + body[1] + " \n" 
	    else: 
	        chunks['body'] = chunks['body'] + body[0] + " \n" 
    # print("Result: ")
    # print(chunks)

    return chunks


