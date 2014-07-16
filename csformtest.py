#!/usr/bin/env python
import array
import pickle
import os
import clr
clr.AddReferenceToFile("ClassLibrary1.dll")
import ClassLibrary1
form = ClassLibrary1.Form1()
contents_list = form.GetContentsList()

contests_def_list = list()
for contents_def in contents_list:
	contests_def = dict()
	print contents_def.start_h
	contests_def['start_h']=contents_def.start_h
	print contents_def.start_m
	contests_def['start_m']=contents_def.start_m
	print contents_def.interval
	contests_def['interval']=contents_def.interval
	contests_def['contents']=list()
	for content in contents_def.contents:
		print content
		contests_def['contents'].append(content)
	contests_def_list.append(contests_def)
		
contests_def_list_str = pickle.dumps(contests_def_list)
print contests_def_list_str


images = dict()
image_file_names = 'images/Jellyfish.jpg','images/Penguins.jpg','images/Chrysanthemum.jpg','images/Desert.jpg','images/Hydrangeas.jpg','images/Lighthouse.jpg','images/Tulips.jpg'
for fpath in image_file_names:
	print("open:" + fpath)
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
	imgstr = pickle.dumps(ar)
	print(imgstr)

imgs_str = pickle.dumps(images)

ClassLibrary1.Form1.uploadConfigAndImages(contests_def_list_str, imgs_str)
