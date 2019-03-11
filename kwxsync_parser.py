'''
    Script: kwxsync_parser.py
    Desc: splits a kwxsync command into smaller (but equivalent) 'packages'.
    Developed By: www.emenda.se

    v1.0
        - Initial Release

'''

import argparse
import datetime
import os
import sys
import re
import json
from datetime import datetime
import socket
import ssl
import itertools
if sys.version_info >= (3, 0):
    import urllib.parse
    import urllib.request
else:
    import urllib
    import urllib2
    import ssl

g_version = 1.0
g_projects = "A B C D"
g_rest = """--statuses "Analyze","Ignore","Not a problem","Fix","Fix in Next Release","Defer","Filter" --last-sync "05-03-2016 00:00:00" --host ***REMOVED*** --port 8080"""

# Logging messages to the console
def output(message, severity=''):
    if severity is None or severity == '':
        print('[' + str(datetime.now().strftime('%Y-%m-%d  %H:%M:%S')) + ']: ' + message)
    else:
        print('[' + str(datetime.now().strftime('%Y-%m-%d  %H:%M:%S')) + '] ' + severity + ': ' + message)


# Message to be displayed on start
def start_message(filename, version, args=None):
    print('--------------------------------------------------------------------------------')
    print(filename + '    version: ' + str(version) + '    created by: Emenda Nordic AB')
    print('--------------------------------------------------------------------------------')
    if args:
        for k in args.keys():
            print("%s: %s" % (k, args[k]))
        print('--------------------------------------------------------------------------------')

#input: A, B, C, D
#output: {A,B}, {A,C}, {A,D}, {B,C}, {B,D}, {C,D}
def create_project_tuples(g_projects):
    a = "".join(g_projects.split())
    tup = tuple(a)
    print(tup)
    things = itertools.combinations_with_replacement(tup, 2)
    results = [x for x in itertools.combinations(tup, 2) ]
    print(results)
    return results
    
def construct_kwxsync_commands(project_tuples, g_rest):
    commandList = []
    for project_tup in project_tuples:
        command = "kwxsync %s" % g_rest
        for proj in project_tup:
            command += " %s" % proj 
        #print(command)
        commandList.append(command)
    for command in commandList:
        print(command)
    return False


def main():
    global g_rest, g_projects
    #set_global_data()
    start_message(os.path.basename(__file__), g_version, {'projects': g_projects, 'rest': g_rest})
    error = False
    project_tuples = create_project_tuples(g_projects)
    construct_kwxsync_commands(project_tuples, g_rest)

if __name__ == '__main__':
    main()