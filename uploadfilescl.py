#!/usr/bin/env python
import array
import sys
import os
import pickle

from pysimplesoap.client import SoapClient, SoapFault
from pysimplesoap.simplexml import SimpleXMLElement

# create a simple consumer
client = SoapClient(
    location = "http://localhost:8008/",
    action = 'http://localhost:8008/', # SOAPAction
    namespace = "http://example.com/sample.wsdl", 
    soap_ns='soap',
    trace = True,
    ns = False)

images = dict()
for i in range(1, len(sys.argv)):
	fpath = sys.argv[i]
	print("(" + str(i) + ")open:" + fpath)
	name = os.path.split(fpath)
	name_ext = os.path.splitext(name[1])
	fname = name_ext[0]
	fext = name_ext[1]
	images[fname + fext] = array.array('B')
	ar = images[fname + fext]
	with open(fpath, 'rb') as f:
		#print(f)
		while True:
			try:
				ar.fromfile(f, 1024)
			except EOFError:
				break
#	imgstr = pickle.dumps(ar)
#	print(imgstr)
#	client.uploadImage(name=fname+fext, imgstr=imgstr)

# call the remote method
imgs_str = pickle.dumps(images)
#print(imgsstr)
#client.uploadImages(imgs_str=imgs_str)
contests_def_list = list()
contests_def_1 = dict()
contests_def_1['start_h']=0
contests_def_1['start_m']=0
contests_def_1['interval']=60
contests_def_1['contents']=('Jellyfish.jpg','Penguins.jpg')
contests_def_list.append(contests_def_1)
contests_def_2 = dict()
contests_def_2['start_h']=12
contests_def_2['start_m']=0
contests_def_2['interval']=60
contests_def_2['contents']=('Tulips.jpg','Hydrangeas.jpg','Chrysanthemum.jpg')
contests_def_list.append(contests_def_2)
contests_def_3 = dict()
contests_def_3['start_h']=18
contests_def_3['start_m']=0
contests_def_3['interval']=60
contests_def_3['contents']=('Desert.jpg','Lighthouse.jpg')
contests_def_list.append(contests_def_3)
contests_def_list_str = pickle.dumps(contests_def_list)
#print contests_def_list_str
client.uploadConfigAndImages(contests_def_list_str=contests_def_list_str, imgs_str=imgs_str)


