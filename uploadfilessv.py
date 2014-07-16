#!/usr/bin/env python
from pysimplesoap.server import SoapDispatcher, SOAPHandler
from BaseHTTPServer import HTTPServer
from pysimplesoap.simplexml import SimpleXMLElement
 
import pickle
import array
import gtk, gobject
import thread, time

#global
g_current_content_def = dict()
g_contenf_def_list = list()
g_last_content_update_time = time.time()
g_current_content_idx = -1

class TestWindow:
	# This is a callback function. The data arguments are ignored
	# in this example. More on callbacks below.
	def hello(self, widget, data=None):
		print "Hello World"

	def delete_event(self, widget, event, data=None):
		# If you return FALSE in the "delete_event" signal handler,
		# GTK will emit the "destroy" signal. Returning TRUE means
		# you don't want the window to be destroyed.
		# This is useful for popping up 'are you sure you want to quit?'
		# type dialogs.
		print "delete event occurred"

		# Change FALSE to TRUE and the main window will not be destroyed
		# with a "delete_event".
		return False

	# Another callback
	def destroy(self, widget, data=None):
		gtk.main_quit()

	def __init__(self):
		# create a new window
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

		# When the window is given the "delete_event" signal (this is given
		# by the window manager, usually by the "close" option, or on the
		# titlebar), we ask it to call the delete_event () function
		# as defined above. The data passed to the callback
		# function is NULL and is ignored in the callback function.
		self.window.connect("delete_event", self.delete_event)

		# Here we connect the "destroy" event to a signal handler.
		# This event occurs when we call gtk_widget_destroy() on the window,
		# or if we return FALSE in the "delete_event" callback.
		self.window.connect("destroy", self.destroy)

		# Sets the border width of the window.
		self.window.set_border_width(10)

		# Creates a labels
		self.label_time = gtk.Label("time")
		self.label_content = gtk.Label("content")

		# This packs the button into the window (a GTK container).
		self.pane = gtk.VPaned()
		self.pane.add(self.label_time)
		self.pane.add(self.label_content)
		self.window.add(self.pane)

		# The final step is to display this newly created widget.
		self.label_time.show()
		self.label_content.show()
		self.pane.show()

		# and the window
		self.window.show()

	def main(self):
		# All PyGTK applications must have a gtk.main(). Control ends here
		# and waits for an event to occur (like a key press or mouse event).
		print "Entering gtk.main()..."
		gtk.main()

def callback(httpd):
	print "enter callback"
	global g_test_window
	g_test_window.label_time.set_text(time.ctime())

	#check contents definition
	nowtime = time.localtime()
	now_h = nowtime.tm_hour
	now_m = nowtime.tm_min
	h = 0
	m = 0
	global g_contenf_def_list, g_current_content_def, g_current_content_idx, g_last_content_update_time
	for contents_def in g_contenf_def_list:
		start_h = contents_def['start_h']
		start_m = contents_def['start_m']
		if start_h >= h and start_h <= now_h :
			if start_m >= m and start_m <= now_m :
				h = start_h
				m = start_m
				interval = contents_def['interval']
				contents = contents_def['contents']
				g_current_content_def = contents_def
	
	#show current content
	if len(g_current_content_def) > 0 :
		print 'start time=%(h)02d:%(m)02d' % {"h": g_current_content_def['start_h'], "m": g_current_content_def['start_m']}
		print 'interval=%(interval)d' % {"interval": g_current_content_def['interval']}
		content_idx = 0
		for content in g_current_content_def['contents']:
			print ' %(content_idx)d : %(content)s' % {"content_idx": content_idx, "content": content}
			content_idx = content_idx + 1
	
	#check interval and change contents
	time_diff = time.time() - g_last_content_update_time
	print "past from last update: %(time_diff)d" % {"time_diff": time_diff}
	if len(g_current_content_def) > 0 :
		interval = g_current_content_def['interval']
		if interval < time_diff or g_current_content_idx == -1:
			contents = g_current_content_def['contents']
			i = iter(contents)
			index = 0
			g_current_content_idx = g_current_content_idx + 1
			for content_name in i:
				if index == g_current_content_idx:
					g_test_window.label_content.set_text(content_name)
					g_last_content_update_time = time.time()
					break;
				else :
					index = index + 1			
	
	#handle web serice request
	httpd.handle_request()
	#The function is called repeatedly until it returns FALSE 
	return True

# Define a function for Web Service
def uploadConfigAndImages(contests_def_list_str, imgs_str):
	#print(conf_dic_str)
	with open("out\\contents_def.dat", 'wb') as f1:
		f1.write(contests_def_list_str)
	with open("out\\imgs.dat", 'wb') as f2:
		f2.write(imgs_str)
	global g_contenf_def_list
	g_contenf_def_list = pickle.loads(contests_def_list_str)
	for contents_def in g_contenf_def_list:
		start_h = contents_def['start_h']
		start_m = contents_def['start_h']
		print 'start time=%(h)02d:%(m)02d' % {"h": start_h, "m": start_m}
		interval = contents_def['interval']
		print 'interval=%(interval)d' % {"interval": interval}
		contents = contents_def['contents']
		content_idx = 0
		for content in contents:
			print ' %(content_idx)d : %(content)s' % {"content_idx": content_idx, "content": content}
			content_idx = content_idx + 1
	
	imgs = pickle.loads(imgs_str)
	for image_name in iter(imgs):
		print(image_name)
		ar = imgs[image_name]	
		with open("out/" + image_name, 'wb') as f3:
			ar.tofile(f3)
	return 0

def uploadImages(imgsstr):
	#print(imgsstr)
	imgs = pickle.loads(imgsstr)
	for image_name in iter(imgs):
		print(image_name)
		ar = imgs[image_name]	
		with open("out\\" + image_name, 'wb') as f2:
			ar.tofile(f2)
	return 0

def uploadImage(name, imgstr):
	try:
		print(name)
		print(imgstr)
		img = pickle.loads(imgstr)
		#xmlElm = SimpleXMLElement("<xmlElm><a>" + imgxmlstr + "</a></xmlElm>")
		#print(xmlElm.children())
		#img = xmlElm.unmarshall({'img':array.array})
		print(img)
		with open("out\\" + name, 'wb') as f2:
			img.tofile(f2)
	except Exception as e:
		print e
	return 0

# If the program is run directly or passed as an argument to the python
# interpreter then create a server instance and show window
if __name__ == "__main__":
	dispatcher = SoapDispatcher(
		'my_dispatcher',
		location = "http://localhost:8008/",
		action = 'http://localhost:8008/', # SOAPAction
		namespace = "http://example.com/sample.wsdl", prefix="ns0",
		trace = True,
		ns = True)

	# register the user function
	dispatcher.register_function('uploadImages', uploadImages, 
		returns={'Result': int},
			args={'imgs_str': str})

	dispatcher.register_function('uploadImage', uploadImage, 
		returns={'Result': int},
			args={'name': str, 'imgstr': str})

	dispatcher.register_function('uploadConfigAndImages', uploadConfigAndImages, 
		returns={'Result': int},
			args={'contests_def_list_str': str, 'imgs_str': str})

	print "Starting server..."
	httpd = HTTPServer(("", 8008), SOAPHandler)
	httpd.dispatcher = dispatcher
	httpd.timeout = 1
	#httpd.serve_forever()
	
	gobject.timeout_add_seconds(2, callback, httpd)

	g_test_window = TestWindow()
	g_test_window.main()

