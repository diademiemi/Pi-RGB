#!/usr/bin/env python3

import socket
import os
from dotenv import load_dotenv

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--address", help="Specify address used to connect, falls back to .env file, defaults to 127.0.0.1", action="store")
parser.add_argument("-p", "--port", help="Specify port used to connect, falls back to .env file, defaults to 5807", action="store", type=int)
parser.add_argument("-t", "--time", help="Time between colours in sequences such as strobe, breathe and fade, supports decimals, defaults to 1 second", action="store", type=float)
cparser = parser.add_mutually_exclusive_group(required=True)
cparser.add_argument("-c", "--colour", "--color", help="Send colour to daemon. Accepts CSS colour or hex value prefixed with #", action="store")
cparser.add_argument("-s", "--strobe", help="Send strobe pattern to daemon. Accepts CSS colours or hex values prefixed with # in a comma seperated string", action="store")
cparser.add_argument("-f", "--fade", help="Send fade pattern to daemon. Accepts CSS colours or hex values prefixed with # in a comma seperated string", action="store")
cparser.add_argument("-b", "--breathe", help="Send breathe pattern to daemon. Accepts CSS colours or hex values prefixed with # in a comma seperated string", action="store")

load_dotenv()

args = parser.parse_args()

# Load address and port from argument, if that fails, .env, if that fails, fall back to 127.0.0.1
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


# Main function, this sends the data to the daemon process
def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	if args.colour:
		data = "single,{0}".format("".join(args.colour.replace('#', '').split(',', 1)[0])).encode('ascii')
	if args.strobe:
		data = "strobe,{0},{1}".format(time, "".join(args.strobe.replace('#', '').split())).encode('ascii')
	if args.fade:
		data = "fade,{0},{1}".format(time, "".join(args.fade.replace('#', '').split())).encode('ascii')
	if args.breathe:
		data = "breathe,{0},{1}".format(time, "".join(args.breathe.replace('#', '').split())).encode('ascii')

	sock.sendto(data, (address, port))

if __name__ == "__main__":
	main()
