########################################################################
#                                                                      #
#          NAME:  LMODEM - Send File                                   #
#  DEVELOPED BY:  Chris Clement (K7CTC)                                #
#       VERSION:  v0.2                                                 #
#                                                                      #
########################################################################

#import from project library
from multiprocessing import current_process
import lostik
from console import console

#import from standard library
import textwrap
import lzma
import argparse
from base64 import b85encode
from time import sleep
from pathlib import Path
from hashlib import blake2b

#establish and parse command line arguments
parser = argparse.ArgumentParser(description='LMODEM - Send File',
                                 epilog='Created by K7CTC.')
parser.add_argument('outgoing_file')
args = parser.parse_args()
del parser

#check if outgoing file actually exists
if not Path(args.outgoing_file).is_file():
    print(f'[ERROR] {args.outgoing_file} does not exist in current working directory!')
    exit(1)

#LMODEM maximum file name length will henceforth be limited to 32 characters
if len(args.outgoing_file) > 32:
    print('[ERROR] File name exceeds 32 character limit!')
    print('HELP: Come on, this is LoRa we are working with here.')
    exit(1)

#get size of outgoing file
outgoing_file_size = Path(args.outgoing_file).stat().st_size

#get secure hash for outgoing file
with open(args.outgoing_file, 'rb') as file:
    outgoing_file_secure_hash = blake2b(digest_size=32)
    outgoing_file_secure_hash.update(file.read())

#compress outgoing file
with open(args.outgoing_file, 'rb') as file:
    outgoing_file_compressed = lzma.compress(file.read())
#base85 encode compressed outgoing file
outgoing_file_compressed_b85 = b85encode(outgoing_file_compressed)
#hex encode base85 encoded compressed outgoing file
outgoing_file_compressed_b85_hex = outgoing_file_compressed_b85.hex()

#split hex encoded base85 encoded compressed outgoing file into 128 byte blocks
outgoing_file_blocks = textwrap.wrap(outgoing_file_compressed_b85_hex, 256)

#LMODEM maximum OTA file size will henceforth be limited to 32kb
if len(outgoing_file_compressed_b85) > 32768:
    print('[ERROR] Compressed file exceeds maximum size of 32,768 bytes!')
    print('HELP: Come on, this is LoRa we are working with here.')
    exit(1)

#show file transfer details
console.clear()
print('File Transfer Details - Outgoing File')
print('-------------------------------------')
print(f'       Name: {args.outgoing_file}')
print(f'       Size: {outgoing_file_size} bytes (on disk) / {len(outgoing_file_compressed_b85)} bytes (over-the-air)')
print(f'Secure Hash: {outgoing_file_secure_hash.hexdigest()}')
print(f'     Blocks: {len(outgoing_file_blocks)}')
print()

#provide receiving station with the file transfer details
#  file name
#  number of blocks
#  secure hash
packet = args.outgoing_file + '|' + str(len(outgoing_file_blocks)) + '|' + outgoing_file_secure_hash.hexdigest()
print('Sending file transfer details to receiving station...')
lostik.tx(packet, encode=True)





# #listen for acknowledgement
# lostik.await_ack()
# print('Acknowledgement received.  Begin file transfer...')

# for block in blocks:
#     lostik.tx(block)
#     current_block = blocks.index(block) + 1
#     print(f'Sent block {current_block} of {len(blocks)}')
#     sleep(.25)
#     # lostik.await_ack()

# #send OEF (end of file) message
# lostik.tx('454F46')
# print('DONE!')
# print()
