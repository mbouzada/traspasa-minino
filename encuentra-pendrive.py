#!/usr/bin/python3

import sys
import subprocess

udisk = subprocess.Popen('udisksctl dump', shell=True, stdout=subprocess.PIPE)
datos = ""
while udisk.poll() is None:
	(a,b) = udisk.communicate()
	datos += a.decode("utf-8")
datos = datos.split("/org/freedesktop/UDisks2/drives")

tofind = []

for elemento in datos:
	lineas = elemento.split("\n")
	vendor = None
	id = None
	model = None
	usb = False
	for linea in lineas:
		pos = linea.find(":")
		if pos == -1:
			continue
		key = linea[:pos+1].strip()
		data = linea[pos+1:].strip()
		if key == "ConnectionBus:" and data == "usb":
			usb = True
			continue
		if key == "Model:":
			model = data
			continue
		if key == "Vendor:":
			vendor = data
			continue
		if key == "Id:":
			id = data
			continue
	if (vendor is not None) and (model is not None) and (id is not None) and usb:
		tofind.append( (id,vendor,model) )

for disk in tofind:
	id = disk[0]
	vendor = disk[1]
	model = disk[2]
	for elemento in datos:
		lineas = elemento.split("\n")
		path = None
		id2 = None
		for linea in lineas:
			pos = linea.find(":")
			if pos == -1:
				continue
			key = linea[:pos+1].strip()
			data = linea[pos+1:].strip()
			if key == "Id:":
				id2 = data
				continue
			if key == "MountPoints:":
				path = data
				continue

		if (id2 is not None) and (id2 == "by-id-usb-"+id.replace("-","_")+"-0:0-part1"):
			print("{:s} {:s}, {:s}".format(vendor,model,path))
