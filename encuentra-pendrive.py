#!/usr/bin/python3

import sys
import subprocess
import dbus

udisk = dbus.SystemBus().get_object('org.freedesktop.UDisks2','/org/freedesktop/UDisks2')
iface = dbus.Interface(udisk, 'org.freedesktop.DBus.ObjectManager')
xml_string = iface.GetManagedObjects()

partitions = []
for objeto in xml_string:
	if not objeto.startswith("/org/freedesktop/UDisks2/block_devices/"):
		continue
	unidad = dbus.SystemBus().get_object('org.freedesktop.UDisks2',objeto)
	iface = dbus.Interface(unidad, 'org.freedesktop.DBus.Properties')
	props = iface.GetAll('org.freedesktop.UDisks2.Block')

	partitions.append(props)
	if props["Drive"] != '/':
		drv = dbus.SystemBus().get_object('org.freedesktop.UDisks2',props["Drive"])
		iface2 = dbus.Interface(drv, 'org.freedesktop.DBus.Properties')
		props2 = iface2.GetAll('org.freedesktop.UDisks2.Drive')
		props["drive_props"] = props2
	else:
		props["drive_props"] = {}

for part in partitions:
	if len(part["drive_props"]) == 0:
		continue
	if part["drive_props"]["ConnectionBus"] != "usb":
		continue
	if not part["drive_props"]["MediaAvailable"]:
		continue
	devname = ''.join([chr(byte) for byte in part["Device"]])
	vendor =  part["drive_props"]["Vendor"]
	model =  part["drive_props"]["Model"]
	if (vendor == ""):
		vendormodel = model
	elif (model == ""):
		vendormodel = vendor
	else:
		vendormodel = "{:s} {:s}".format(vendor, model)
	print("{:s}, {:s}".format(vendormodel,devname))
