#! /usr/bin/env python

import gtk, gobject, webkit
import thread, time

from pysimplesoap.server import SoapDispatcher, SOAPHandler
from BaseHTTPServer import HTTPServer

w = gtk.Window(gtk.WINDOW_TOPLEVEL)
w.connect("destroy", gtk.main_quit)
b = webkit.WebView()
w.add(b)
w.show_all()
w.fullscreen()

# Define a function for timer callback
def callback(httpd):
	#print "waiting httpd.handle_request()..."
    httpd.handle_request()
	#print "exit httpd.handle_request()"
	return True

# Define a function for Web Service
def open(url):
    	print "Open URL" + url
	global b
    	b.open(url)
	return 0

dispatcher = SoapDispatcher(
    'my_dispatcher',
    location = "http://localhost:8008/",
    action = 'http://localhost:8008/', # SOAPAction
    namespace = "http://example.com/sample.wsdl", prefix="ns0",
    trace = True,
    ns = True)

# register the user function
dispatcher.register_function('Open', open, 
	returns={'OpenResult': int},
    	args={'url': str})

print "Starting server..."
httpd = HTTPServer(("", 8008), SOAPHandler)
httpd.dispatcher = dispatcher
httpd.timeout = 1

gobject.timeout_add_seconds(2, callback, httpd)

print "Entering gtk.main()..."
gtk.main()



