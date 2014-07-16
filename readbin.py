#!/usr/bin/env python
import array
import sys
import os

images = dict()
fpath = sys.argv[1]
print("open:" + fpath)
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

#with open("out\\" + fname + fext, 'wb') as f2:
#	ar.tofile(f2)

fpath = sys.argv[2]
print("open:" + fpath)
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

#with open("out\\" + fname + fext, 'wb') as f2:
#	ar.tofile(f2)
for image_name in iter(images):
	ar = images[image_name]	
	with open("out\\" + image_name, 'wb') as f2:
		ar.tofile(f2)
