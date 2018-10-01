#!/usr/bin/python

import urllib
import json
import os
import sys
import getopt
from datetime import datetime
import time
import argparse

TODAY = datetime.now()
TODAY_AS_STR = datetime.strftime(TODAY, '%Y-%m-%d')
FIRST_DATE = datetime.strptime('1995-06-16', '%Y-%m-%d')

API_URL = "https://api.nasa.gov/planetary/apod"
API_PARAMS = '?api_key={}&date={}'

def lookup_image(date, api_key, path):
    """
    Lookup and save image from NASA API based on given date.

    See more on: https://api.nasa.gov/api.html
    :param str date: Valid date as String
    :param str api_key: NASA api key
    :param str path: Path on host to where image will be downloaded
    :return: None
    :raises OSError: if there's no permission to store image (create dir or write image)

    """
    # Create the API url
    api_url = API_URL + API_PARAMS.format(api_key, date)

    # Get the json with metadata of the image
    response = urllib.urlopen(api_url)

    response = json.loads(response.read())
    if not (isinstance(response, dict) and 'url' in response):
        print 'Error parsing response. Responde json might has changed?'
        sys.exit(2)

    image_url = response.get("url")

    file_extension = os.path.splitext(image_url)[1]

    if path and path[-1] != '/':
        path = path + '/'

    # Try to create the dir (if it not exists)
    try:
        if not os.path.isdir(path):
            os.mkdir(path)
        urllib.urlretrieve(image_url, path + date + file_extension)
        # Permission denied
    except OSError:
        raise 'Permission denied. Please run: sudo <script>.py [options]'
        sys.exit(2)

def valid_date(date):
    """
    Type Validator function for argparse.

    Check date format and valida date range

    :param str date: String containing a date to lookup image
    :return: Valid date as String
    :rtype: str
    :raises ValueError: if non-valid date format passed or
                        out of range date

    """
    try:
        _date = datetime.strptime(date, '%Y-%m-%d')
        if _date > TODAY or _date < FIRST_DATE:
            msg = 'Date out of range [1995-06-16 - today]'
            raise argparse.ArgumentTypeError(msg)
        return date
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("lala")
    parser.add_argument("-d", "--date",
                        help="Format YYYY-MM-DD (default: today)",
                        default=TODAY_AS_STR,
                        type=valid_date)
    parser.add_argument("-k", "--key",
                        help="NASA API key - Get yours at https://api.nasa.gov/index.html#apply-for-an-api-key",
                        required=True)
    parser.add_argument("-p", "--path",
                        help="Path to download image",
                        required=True)

    args = parser.parse_args()
    lookup_image(args.date, args.key, args.path)
