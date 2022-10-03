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




# #set initial LoStik operating parameters
# lostik.lmodem_set_mode(args.mode)
# lostik.lmodem_set_channel(args.channel)

# #check if outgoing file actually exists
# if not Path(args.outgoing_file).is_file():
#     exit(1)

# #check if outgoing file name exceeds LMODEM maximum length of 32 characters
# if len(args.outgoing_file) > 32:
#     exit(1)

# #generate secure hash hex digest for outgoing file
# with open(args.outgoing_file, 'rb') as file:
#     outgoing_file_secure_hash = blake2b(digest_size=16)
#     outgoing_file_secure_hash.update(file.read())
#     outgoing_file_secure_hash_hex_digest = outgoing_file_secure_hash.hexdigest()
# del outgoing_file_secure_hash

# #compress outgoing file (in memory) using lzma algorithm
# with open(args.outgoing_file, 'rb') as file:
#     outgoing_file_compressed = lzma.compress(file.read())

# #base85 encode compressed outgoing file
# outgoing_file_compressed_b85 = b85encode(outgoing_file_compressed)
# del outgoing_file_compressed

# #determine over-the-air outgoing file size in bytes
# outgoing_file_size_ota = len(outgoing_file_compressed_b85)

# print(outgoing_file_size_ota)

# #check if outgoing file size over-the-air exceeds LMODEM maximum for chosen mode
# maximum_ota_file_size = 0
# if args.mode == 1:
#     maximum_ota_file_size = 49152
# if args.mode == 2:
#     maximum_ota_file_size = 32768
# if args.mode == 3:
#     maximum_ota_file_size = 16384   
# if outgoing_file_size_ota > maximum_ota_file_size:
#     print(f'[red1 on deep_sky_blue4][ERROR][/] Size (over the air) exceeds maximum of {maximum_ota_file_size} bytes for mode {args.mode}!')
#     exit(1)
# del maximum_ota_file_size

# #determine on disk outgoing file size in bytes
# outgoing_file_size_on_disk = Path(args.outgoing_file).stat().st_size

# print(outgoing_file_size_on_disk)

# #hex encode base85 encoded compressed outgoing file
# outgoing_file_compressed_b85_hex = outgoing_file_compressed_b85.hex()

# del outgoing_file_compressed_b85

# #split hex encoded base85 encoded compressed outgoing file into blocks for chosen mode
# block_size = 0
# if args.mode == 1:
#     block_size = 192 * 2
# if args.mode == 2:
#     block_size = 128 * 2
# if args.mode == 3:
#     block_size = 64 * 2 

# blocks = textwrap.wrap(outgoing_file_compressed_b85_hex, block_size)
# del block_size, outgoing_file_compressed_b85_hex

# block_count = len(blocks)

# #concatenate zero filled block index and block contents to create numbered packets
# packets = []
# for block in blocks:
#     block_index_zfill = str(blocks.index(block)).zfill(3)
#     block_index_zfill_hex = block_index_zfill.encode('ASCII').hex()
#     packet = block_index_zfill_hex + block
#     packets.append(packet)
# del blocks

# def send_requested_blocks(received_block_count, requested_blocks):
#     print('Transmitting requested blocks.')
#     print(datetime.now())
#     for block_number in requested_blocks:
#         time_sent, air_time = lostik.tx(packets[int(block_number)], delay=.15)
#         print(air_time)
#     lostik.tx('REQ_BLOCKS_SENT', encode=True, delay=.15)
#     print(datetime.now())

# print('Starting file transfer.')
# requested_blocks = []
# for packet in packets:
#     requested_blocks.append(packets.index(packet))
# requested_block_count = len(requested_blocks)
# del requested_block_count
# send_requested_blocks(0, requested_blocks)
# del requested_blocks

