#!/usr/bin/python
# -*- coding: utf-8 -*-



""" 
USes my tiny REST library to send messages to everyone.
I'm coming to get you, Barbara...

Victor Perron 02/01/2011

"""

import facebook_rest
import sys


# Open UIDs file
if(len(sys.argv) < 2):
    print "Usage : send_messages <REQUEST_FILE> [UID_FILE]"
    print "UID_FILE is an optional file that keeps a list of all UIDs you want to send a message to,"
    print "provided that your request contains a to=ALL recipient."
    sys.exit(0)


uids = []
if(len(sys.argv) > 2):
    f = open(sys.argv[2],"r")

    for line in f:
        uids.append(line.replace('\n',''))

    f.close()


uid, sessionkey, secret = facebook_rest.authenticate()

commands = facebook_rest.commandsfromfile(sys.argv[1], uid)

for command in commands:

    method  = command[0]
    args    = command[1]

    results = []

    if(method == 'mailbox.send' and args['to'] == 'ALL'):

        pattern = args['body']

        for uid in uids:
            args['to'] = uid

            result = facebook_rest.FBRequest('fql.query',{'query':'SELECT first_name, name FROM user WHERE uid='+uid+';'},sessionkey,secret)

            print "Sending message to UID "+uid+' ( '+result[0]['first_name']+' )'

            args['body'] = pattern.replace("USERNAME",result[0]['first_name'])

            results.append(facebook_rest.FBRequest(method,args,sessionkey,secret))

            break
    else:
        results.append(facebook_rest.FBRequest(method,args,sessionkey,secret))


    print results
