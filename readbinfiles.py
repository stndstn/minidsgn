#!/usr/bin/env python
import array
import sys
import os

def saveimages(imgs):
	for image_name in iter(imgs):
		ar = imgs[image_name]	
		with open("out\\" + image_name, 'wb') as f2:
			ar.tofile(f2)

images = dict()
for i in range(1, len(sys.argv)):
	fpath = sys.argv[i]
	print("(" + str(i) + ")open:" + fpath)
	name_ext = os.path.splitext(fpath)
	fname = name_ext[0]
	fext = name_ext[1]
	images[fname + fext] = array.array('B')
	ar = images[fname + fext]
	with open(fpath, 'rb') as f:
		print(f)
		while True:
			try:
				ar.fromfile(f, 1024)
			except EOFError:
				break


saveimages(images)
