#!/usr/bin/env python3

import argparse
import socket
import yaml
import os
from colour import Color
from dotenv import load_dotenv

# Add command arguments
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--address", help="Specify address used to connect, falls back to .env file, defaults to 127.0.0.1", action="store")
parser.add_argument("-F", "--file", help="YAML file to read for presets, use with -P", action="store")
parser.add_argument("-p", "--port", help="Specify port used to connect, falls back to .env file, defaults to 5807", action="store", type=int)
parser.add_argument("-t", "--time", help="Time between colours in sequences such as strobe, breathe and fade, supports decimals, defaults to 1 second", action="store", type=float)
cparser = parser.add_mutually_exclusive_group(required=True)
cparser.add_argument("-c", "--colour", "--color", help="Send colour to daemon. Accepts CSS colour or hex value prefixed with #", action="store")
cparser.add_argument("-s", "--strobe", help="Send strobe pattern to daemon. Accepts CSS colours or hex values prefixed with # in a comma seperated string", action="store")
cparser.add_argument("-f", "--fade", help="Send fade pattern to daemon. Accepts CSS colours or hex values prefixed with # in a comma seperated string", action="store")
cparser.add_argument("-b", "--breathe", help="Send breathe pattern to daemon. Accepts CSS colours or hex values prefixed with # in a comma seperated string", action="store")
cparser.add_argument("-P", "--preset", help="Load named preset from presets.yaml file", action="store")

load_dotenv()

args = parser.parse_args()

# Load address, port and time from argument, if that fails, .env, if that fails, fall back to 127.0.0.1
if args.address is not None:
	address = args.address
else:
	address = os.getenv('LISTEN_ADDRESS')
	if address is None:
		address = '127.0.0.1'

if args.port is not None:
	port = args.port
else:
	port = int(os.getenv('LISTEN_PORT'))
	if port is None:
		port = 5807

if args.time is not None:
	time = args.time
else:
	time = float(os.getenv('DEFAULT_TIME'))
	if time is None:
		time = float(1)

def format(input):
	colours = input.split(",")
	for colour in colours:
		if colour.startswith("#"):
			yield colour[1:]
		else:
			yield Color(colour).hex_l[1:]
			

# Prepare UDP connection
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Check which argument is given and prepare data
if args.colour:
	c = format(args.colour)
	data = "single,{0}".format(",".join(c)).encode('ascii')
if args.strobe:
	c = format(args.strobe)
	data = "strobe,{0},{1}".format(time, ",".join(c)).encode('ascii')
if args.fade:
	c = format(args.fade)
	data = "fade,{0},{1}".format(time, ",".join(c)).encode('ascii')
if args.breathe:
	c = format(args.breathe)
	data = "breathe,{0},{1}".format(time, ",".join(c)).encode('ascii')

# If the preset argument is given, load the options from the YAML file.  
if args.preset:
	if args.file:
		file = args.file
	else:
		file = "presets.yaml"
	
	# Read YAML file
	stream = open(file, 'r')
	contents = yaml.load(stream, Loader=yaml.FullLoader)

	# Check if a valid type is given
	if contents.get(args.preset).get('type') in ['single', 'strobe', 'fade', 'breathe']:
		type = contents.get(args.preset).get('type')
	else:
		print("Please specify a type in your preset. The following types are availabke: colour, stroble, fade, breathe")
		exit

	# Check if time is specified in the preset
	if contents.get(args.preset).get('time'):
		time = float(contents.get(args.preset).get('time'))

	# Add the colours to a list as strings
	colours = []
	for colour in contents.get(args.preset).get('colours'):
		colours.append(str(colour))
	
	# Format the data in a byte array
	data = "{0},{1},{2}".format(type, time, ",".join(list(format(",".join(colours))))).encode('ascii')

# Send the data to the daemon process
sock.sendto(data, (address, port))

