########################################################################
#                                                                      #
#          NAME:  LMODEM - Send File                                   #
#  DEVELOPED BY:  Chris Clement (K7CTC)                                #
#       VERSION:  v0.5-dev                                             #
#                                                                      #
########################################################################

#standard library imports
import lzma
import textwrap
import argparse
from sys import exit
from hashlib import blake2b
from base64 import b85encode
from pathlib import Path

from datetime import datetime

#related third party imports
import rich.progress

#local application/library specific imports
import lostik

#establish and parse command line arguments
parser = argparse.ArgumentParser(description='LMODEM v0.5-dev',
                                 epilog='Created by Chris Clement (K7CTC).')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-s', '--send', metavar='filename', help='send the specified file')
group.add_argument('-r', '--receive', action='store_true', help='receive an incoming file')
parser.add_argument('-m', '--mode',
                    type=int,
                    choices=[1,2,3],
                    help='LMODEM mode (default: 1)',
                    default=1)
parser.add_argument('-c', '--channel',
                    type=int,
                    choices=[1,2,3],
                    help='LMODEM channel (default: 2)',
                    default=2)
args = parser.parse_args()
del parser
