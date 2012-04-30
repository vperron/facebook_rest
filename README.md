facebook_rest
=============

Quick and dirty python library to interact with Facebook REST API.

Victor Perron 02/01/2011

# Basics

This library is provided to give you an example implementation to process basic
requests to the so-called "Old Rest API", which is in deprecation at the 
moment.

Use it with caution and please forgive me for any mistake, strange behaviour,
bug that could happen.

When in doubt, read the source.

Last introduction words, feel free to adapt, reuse and modify this code as much
as you want !

Legal notice:
http://creativecommons.org/licenses/by-sa/3.0/legalcode


# Usage

The file

> facebook_rest.py 

is the actual "library" and basically provides 3 methods.

> authenticate(

> FBRequest(

> commandsfromfile(


# File format

I have decided to use a special file format to specify the commands one 
would want to pass to the Facebook API.

You can find examples of those files (named \*.cmd) in this folder.

The design is very simple:

> \#COMMAND_A
> key1=arg1
> key2=arg2
> \#COMMAND_B
> key1=arg1
> \#COMMAND_C
> etc...

There is nearly no check for correctness of the above specification, so please
try and stick to it as much as you can !

Moreover, you can define some placeholders in those commands, that will be 
replaced at runtime :

* GIVENUID : in one argument has for effect that this command will be executed 
    with the actual Facebook user\_id of the person who is authenticated (you !)

* USERNAME : is replaced with the first name of the current uid in the request;

* \n : really write it with the backslash, like in a printf format string) will 
    result in a newline when passed to server.
    This has been done in order to allow you for example multiline messages
    while only single-line arguments are specified in the commands file.
