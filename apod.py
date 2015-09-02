#!/usr/bin/python

import urllib
import json
import os
import sys
import getopt
import datetime
import time

def parse_parameters(argv):

	today = time.strftime("%Y-%m-%d")

	path = ''
	date = today
	key = 'DEMO_KEY'
	background = False

	try:
		opts, args = getopt.getopt(argv[1:], "p:d:k:h", ["path=", "date=", "key=", "background"])

	except getopt.GetoptError as err:
		usage()

	except:
		usage()

	for o, a in opts:
		
		if o in ('-p', '--path'):
			path = a
		
		elif o in ('-d', '--date'):

			date = a

			try:

				datetime.datetime.strptime(date, '%Y-%m-%d')

				if not date <= today:
					print 'Date out of range'
					sys.exit(2)

			except ValueError:
				print 'Incorrect data format, should be YYYY-MM-DD'
				usage()

		elif o in ('-k', '--key'):
			key = a

		elif o == '-h':
			usage()

		elif o == '--background':
			background = True

		else:
			usage()

	if len(opts) == 0: usage()

	return {'path': path, 'date': date, 'key' : key, 'background' : background}


def usage():
	print "how to use"
	sys.exit(1)


def get_image(args):
	
	api_url = 'https://api.nasa.gov/planetary/apod?api_key=' + args['key'] + '&date=' + args['date'] + '&format=JSON'

	response = urllib.urlopen(api_url)		

	image_url = json.loads(response.read())['url']

	file_extension = os.path.splitext(image_url)[1]

	path = args['path']
	if path and path[-1] != '/':
		path = path + '/'

	if(path and not os.path.isdir(path)):

		try:
			os.mkdir(path)

		except OSError:
			print 'Permission denied. Please run: sudo <script>.py [options]'
			sys.exit(2)

	try:
		urllib.urlretrieve(image_url, path + args['date'] + file_extension)
		return path + args['date'] + file_extension

	except IOError:
		print 'Permission denied. Please run: sudo <script>.py [options]'
		sys.exit(2)	

def change_background(image):

	path = os.path.abspath(image)

	com = 'gsettings set org.gnome.desktop.background picture-uri \"file://' + path + '\"'
	com = com.encode('utf-8')

	os.system(com)

if __name__ == "__main__":

    args = parse_parameters(sys.argv)
    
    image = get_image(args)

    if(args['background']): 
    	change_background(image)
    
