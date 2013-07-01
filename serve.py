#!/usr/bin/env python
 
import os
import sys
import argparse
import subprocess
import BaseHTTPServer
import CGIHTTPServer
import cgitb; cgitb.enable()  ## This line enables CGI error reporting


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
	server = BaseHTTPServer.HTTPServer
	handler = CGIHTTPServer.CGIHTTPRequestHandler
	server_address = ("", port)
	handler.cgi_directories = [""]
	httpd = server(server_address, handler)
	print 'starting server at %s' % getURL(port)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		print 'goodbye'

def openInBrowser(url):
	subprocess.call(['open', url])

def deploy():
	subprocess.call(['rsync', '-av', '--delete', '--delete-excluded', '--exclude', '*.DS_Store', '-e', 'ssh', './public/', 'user@example.com:path/to/docroot/'])

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