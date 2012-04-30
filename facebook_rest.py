#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
Micro-library, provided as a proof-of-concept to 
'communicate' with FB Rest Server without any proxy.

Just paste your API Key and Secret and enjoy.

Victor Perron 02/01/2011
"""



import time, math
import hashlib
import urllib
import sys
import re
import getopt

"""
DEFINITIONS
"""

# Paste here your own api keys & secret
API_KEY         = "your_own_api_key"
API_SECRET      = "your_own_api_secret"


# User identity
USER_LOGIN      = "your@email"
USER_PASSWORD   = "yourpassword"





# Other definitions
FB_BASE_URL     = "http://api.facebook.com/restserver.php"
FB_SEC_BASE_URL = "https://api.facebook.com/restserver.php"



silent = true
send   = true
"""
METHODS
"""

def generateSignature(params, secret):

    H = hashlib.md5()
    for p in params:
        H.update(p)

    H.update(secret)

    return H.hexdigest()


def authenticate():
    params  = {'email':USER_LOGIN, 'password':USER_PASSWORD}
    answers = FBRequest('auth.login', params, '', '')
    return answers[0]



def getTimestampMilliseconds():
    return str(int(math.floor(time.time()*1000)))


def FBRequest(method, params, sessionkey,secret):
    
    if(silent == False):
        print 'FBRequest called ('+method+').'

    localparams = []

    for key, value in params.iteritems():
        localparams.append(key+'='+value)


    url         = ''

    
    # Base URL and eventually timestamp, millisecond-sharp
    if(method.startswith("auth")):
        url     += FB_SEC_BASE_URL
        localparams.append('api_key='+API_KEY)
        localparams.append('migrations_override={\'empty_json\': true}')
        localparams.append('v=1.0')

    else:
        url     += FB_BASE_URL
        call_id  = "call_id="+getTimestampMilliseconds()

        localparams.append('session_key='+sessionkey)
        localparams.append(call_id)
    
    # Api key, method, format and migrations param: always needed
    localparams.append('api_key='+API_KEY)
    localparams.append('format=JSON')
    localparams.append('method='+method)
    localparams.append('migrations_override={\'empty_json\': true}')
    localparams.append('v=1.0')

    localparams.sort()

    # Generate signature
    if(len(secret) == 0):
        sig = generateSignature(localparams, API_SECRET) # Auth secret, from app registration
    else:
        sig = generateSignature(localparams, secret) # FB Api has a 'temporary' secret after logon
    
    localparams.append('sig='+sig)
    
    localparams.sort()

    # Now build request string
    for param in localparams[:-1]:
        url += param + '&'

    paramdic = {}
    for pair in [item.split('=',1) for item in localparams]:
        k, v  = pair[0], pair[1]
        paramdic[k] = v
        


    urlparams = urllib.urlencode(sorted(paramdic.items()))




    # Read the server's answer
    if(urlparams.find('to=')==-1 or send == True):
        f = urllib.urlopen(url,urlparams)
        # Parse and return it
        answers = f.read()
    else:
        print "Skipped sending mail."
        answers=''

    if(silent == False):
        print "REQ_URL : "+url
        print 'PARAMS: '+str(urlparams)
        print "ANSWERS: "+answers

    answerdic = []

    if(answers.find("error_code") != -1):
        return answerdic

    # Parse the answer
    r = re.compile(r"{(.*?)}")

    answers = r.findall(answers)


    # For each record, f.eg a "Friend", many values can be returned according to the
    # number of properties asked for (first name, picture, ...)
    for answer in answers:
        properties  = answer.split(',')
        dic = {}
        for string in properties:
            pair         = string.split('\":')
            pair[0]      = pair[0].replace("\"",'')
            dic[pair[0]] = pair[1].replace("\"",'')
        answerdic.append(dic)

    #print answerdic
    return answerdic

    


def printUsage(name):
    print "Usage:\n"
    print name+" <ACTION_NAME> [args|path_to_file]"
    print "ACTION_NAME is the name of the REST method you want to execute."
    print "args is a space-separated list of KEY=VALUE pairs, e.g. email=victor@mindslicer.com"
    print "\nThis script will then execute the action and display the resulting output on console."



"""
    Takes a filename as input.
    This file consists in a row of command lines.
    Scheme is:
        #METHOD
        ARGS
        #METHOD
        ARGS
    where ARGS is a comma-separated string of key=value pairs.
"""
def commandsfromfile(filename):
    
    commands = []
    
    f = open(filename,'r')

    line = f.readline()

    while True:
        if(len(line) == 0):
            break;
        
        # Personal placeholders
        line  = line.replace('\n','')
        #line  = line.replace('\\n','%0a')

        if(line[0] == '#'):
            method = line[1:]
            
            args   = {}

            while True:
                argline  = f.readline()

                argline  = argline.replace('\n','').replace('\\n','\n')
                #argline  = argline.replace('\\n','%0a')
                if(len(argline) == 0 or argline[0] == '#'):
                    line = argline;
                    break;

                pair = argline.split('=',1)
                args[pair[0]] = pair[1]
            
            commands.append([method,args])

    f.close()

    return commands


def main():
    # parse command line options
    try:
        # -o is to be followed by an argument, so we put o: in the string
        opts, args = getopt.getopt(sys.argv[1:], "ho:", ["help"])
    except getopt.error, msg:
        print "Error parsing arguments: "+str(msg)
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            printUsage(sys.argv[0])
            sys.exit(0)

    if(len(args) > 1):
        printUsage(sys.argv[0])


    # Authentication
    answers    = authenticate()
    uid        = answers['uid']
    sessionkey = answers['session_key']
    secret     = answers['secret']
    token      = answers['access_token']

    # Read command from command file
    commands = commandsfromfile(args[0])


    # Send them to server
    for command in commands:
        method  = command[0]
        args    = command[1]
    
        localargs = args.copy()

        for k,v in args.items():
            if(isinstance(v,basestring)):
                arg = v.replace('GIVENUID',uid).replace('\\n','\n')
                localargs[k] = arg

        results = FBRequest(method,localargs,sessionkey,secret,token)

        for result in results:
            for key, value in result.items():
                print str(value)


if __name__ == "__main__":
    main()
