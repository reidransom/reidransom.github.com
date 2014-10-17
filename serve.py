#!/usr/bin/env python

import os
import sys
import argparse
import subprocess

# SSH Deploy Destination:
destination = 'reidransom@reidransom.webfactional.com:webapps/reidransom/'

def parseArgs():
    parser = argparse.ArgumentParser(description="Run a static site development http server.")
    parser.add_argument('--deploy', action='store_const', default=False, const=True, dest='deploy', help='sync with the production server')
    parser.add_argument('-s', '--serve', action='store_const', default=False, const=True, dest='serve', help='start the http server')
    parser.add_argument('-o', '--open', action='store_const', default=False, const=True, dest='open', help='open the root url in the default browser')
    parser.add_argument('-p', '--port', action='store', default=8000, metavar='PORT', dest='port', help='port number to run the http server on')
    parser.add_argument('-d', '--docroot', action='store', default="./public", metavar='DOCROOT', dest='docroot', help='directory where files will be served from')
    return parser.parse_args()

def getURL(port):
    return 'http://localhost:%d/' % port

def serve(port, docroot):
    os.chdir(docroot)
    subprocess.call(['http-server', '-p', str(port)])

def openInBrowser(url):
    try:
        subprocess.call(['open', url])
    except FileNotFoundError:
        pass

def deploy():
    subprocess.call(['rsync', '-av', '--delete', '--delete-excluded', '--exclude', '*.DS_Store', '-e', 'ssh', './public/', destination])

def run():
    args = parseArgs()
    if args.deploy == True:
        deploy()
    if args.open == True:
        openInBrowser(getURL(args.port))
    if args.serve == True:
        serve(args.port, args.docroot)
    if len(sys.argv) < 2:
        openInBrowser(getURL(args.port))
        serve(args.port, args.docroot)

if __name__ == "__main__":
    run()
