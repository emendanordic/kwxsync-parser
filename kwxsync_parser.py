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
g_projects = ""
g_commands = ""
g_sleep = ""
g_indicator = False

parser = argparse.ArgumentParser(prog=os.path.basename(__file__),
                                 description="returns several kwxsync commands for a given kwxsync command")
parser.add_argument('-c', "--command", nargs='?', required=True, metavar="all kwxsync arguments", help="kwxsync command arguments, e.g. '""""--statuses "Analyze","Ignore","Not a problem","Fix","Fix in Next Release","Defer","Filter" --last-sync "05-03-2016 00:00:00" --host test.net --port 8080'""")
parser.add_argument('-p', "--projects", nargs='?', required=True, metavar="list of projects", help="lists of projects with which to perform kwxsync across")
parser.add_argument('-s', "--sleep", nargs='?', required=False, metavar="sleep command", help="provide sleep command if you wish to pause between each call to kwxsync, e.g. 'sleep(2)'")
parser.add_argument('-i', "--indicator", action="store_true", help="use if you wish to receive an indication of progress")

# Message to be displayed on start
def start_message(filename, version, args=None):
    print('--------------------------------------------------------------------------------')
    print(filename + '    version: ' + str(version) + '    created by: Emenda Nordic AB')
    print('--------------------------------------------------------------------------------')
    if args:
        for k in args.keys():
            print("%s: %s" % (k, args[k]))
        print('--------------------------------------------------------------------------------')

def create_project_tuples(g_projects):
    a = g_projects.split(" ")
    tup = tuple(a)
    results = [x for x in itertools.combinations(tup, 2) ]
    return results
    
def construct_kwxsync_commands(project_tuples, g_commands):
    commandList = []
    for project_tup in project_tuples:
        command = "kwxsync %s" % g_commands
        for proj in project_tup:
            command += " %s" % proj 
        commandList.append(command)
    return commandList

# Open file
def open_file(name, x):
    try:
        f = open(name, x)
    except IOError as e:
        output("ERROR: %s" % e, level.ERROR)
        end_message(1)
    return f

def writeOutputToFile(f, commandList):
    progressInt = 1
    numberCommands = len(commandList)
    for command in commandList:
        f.write(command + "\n")
        if g_sleep:
            f.write(g_sleep+ "\n")
        if g_indicator:
            progressNotification="echo %s/%s kwxsync commands executed." %(progressInt, numberCommands)
            f.write(progressNotification + "\n")
            progressInt=progressInt+1
# Message to be displayed at end of execution
def end_message(code):
    if code == 0:
        print('--------------------------------------------------------------------------------')
        print('FINISHED: SUCCESSFUL')
        print('kwxsync commands have been saved in file: kwxsync_commands.out')
        print('--------------------------------------------------------------------------------')
    else:
        print('--------------------------------------------------------------------------------')
        print('FINISHED: FAILED')
        print('--------------------------------------------------------------------------------')
    sys.exit(code)

def main():
    global g_commands, g_projects, g_sleep, g_indicator
    args = parser.parse_args()
    g_commands = args.command
    g_projects = args.projects
    g_sleep = args.sleep
    g_indicator = args.indicator
    start_message(os.path.basename(__file__), g_version, {'projects': g_projects, 'command': g_commands})
    project_tuples = create_project_tuples(g_projects)
    commandList = construct_kwxsync_commands(project_tuples, g_commands)
    f = open_file("kwxsync_commands.out", "w+")
    writeOutputToFile(f, commandList)
    end_message(0)
if __name__ == '__main__':
    main()