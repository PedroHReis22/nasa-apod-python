#!/usr/bin/python

import urllib
import json
import os
import sys
import getopt
import datetime
import time

#parse and validate the command line arguments
def parse_parameters(argv):

	#get the current date and the first date of APOD image
	today = time.strptime(time.strftime('%Y-%m-%d'), '%Y-%m-%d')
	first_date = time.strptime('1995-06-16', '%Y-%m-%d')

	path = ''
	date = today
	key = 'DEMO_KEY'

	#parse tge args
	try:
		opts, args = getopt.getopt(argv[1:], 'p:d:k:h', ['path=', 'date=', 'key='])

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

				#verify the date format and range
				datetime.datetime.strptime(date, '%Y-%m-%d')
				date = time.strptime(date, '%Y-%m-%d')

				if date > today or date < first_date:
					print 'Date out of range [1995-06-16 - today]'
					sys.exit(2)

			except ValueError:
				print 'Incorrect data format, should be YYYY-MM-DD'
				usage()

		elif o in ('-k', '--key'):
			key = a

		elif o == '-h':
			usage()

		else:
			usage()

	if len(opts) == 0: usage()

	return {'path': path, 'date': date, 'key' : key}


def usage():

	print """<script>.py [options]
    -d, --date= the date of the Astronomy Picture (YYYY-MM-DD)
    -h show this help
    -k, --key = the key of NASA APOD API
    -p, --path= the image destination path"""

	sys.exit(2)


def get_image(args):

	formated_date = time.strftime('%Y-%m-%d', args['date'])
	
	#create the API url
	api_url = 'https://api.nasa.gov/planetary/apod?api_key=' + args['key'] + '&date=' + formated_date + '&format=JSON'

	#get the json with metadata of the image
	response = urllib.urlopen(api_url)		

	#get the image URL
	image_url = json.loads(response.read())['url']

	file_extension = os.path.splitext(image_url)[1]

	path = args['path']
	if path and path[-1] != '/':
		path = path + '/'

	#try to create the dir (if it not exists)
	if(path and not os.path.isdir(path)):

		try:
			os.mkdir(path)

		#permission denied
		except OSError:
			print 'Permission denied. Please run: sudo <script>.py [options]'
			sys.exit(2)

	#save the image on the selected destination
	try:
		urllib.urlretrieve(image_url, path + formated_date + file_extension)

	except IOError:
		print 'Permission denied. Please run: sudo <script>.py [options]'
		sys.exit(2)	

if __name__ == "__main__":

    args = parse_parameters(sys.argv)
    
    get_image(args)