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
import base64
import textwrap
import lzma
import argparse
from time import sleep
from pathlib import Path
from hashlib import blake2b

#establish and parse command line arguments
parser = argparse.ArgumentParser(description='LMODEM - Send File',
                                 epilog='Created by K7CTC.')
parser.add_argument('outgoing_file')
args = parser.parse_args()
del parser

#note: file name cannot contain spaces (for obvious reasons)

#check if specified file actually exists
if not Path(args.outgoing_file).is_file():
    print(f'[ERROR] {args.outgoing_file} does not exist in current working directory!')
    exit(1)

#really long file names could be problematic so let's set the maximum length to 32 characters
if len(args.outgoing_file) > 32:
    print('[ERROR] File name exceeds 32 character limit!')
    print('HELP: Come on, this is LoRa we are working with here.')
    exit(1)

#get size of source file (in bytes)
file_size = Path(args.outgoing_file).stat().st_size

#base64 encode outgoing file
with open(args.outgoing_file, 'rb') as file:
    b64_bytes = base64.b64encode(file.read())

#compress base64 encoded file
b64_bytes_compressed = lzma.compress(b64_bytes)
del b64_bytes

#get compressed file size (in bytes)
compressed_file_size = len(b64_bytes_compressed)

#make sure file is not too big to send
if compressed_file_size > 32768:
    print('[ERROR] Compressed file exceeds maximum size of 32,768 bytes!')
    exit(1)

#encode compressed base64 encoded file as a hex string
hex_string_compressed = b64_bytes_compressed.hex()
del b64_bytes_compressed

#split hex string into 128 byte blocks (2 hex characters = 1 byte)
blocks = textwrap.wrap(hex_string_compressed, 256)
del hex_string_compressed

#obtain secure hash for outgoing file
with open(args.outgoing_file, 'rb') as file:
    secure_hash = blake2b(digest_size=32)
    secure_hash.update(file.read())

#ui
console.clear()
print(f'    Outgoing File Name: {args.outgoing_file}')
print(f'             File Size: {file_size} bytes')
print(f'File Size (compressed): {compressed_file_size} bytes')
print(f' Secure Hash (BLAKE2b): {secure_hash.hexdigest()}')
print(f'                Blocks: {len(blocks)}')
print()

#provide receiving station with the file transfer details
#  file name
#  number of blocks
#  secure hash
packet = args.outgoing_file + '|' + str(len(blocks)) + '|' + secure_hash.hexdigest()
print('Sending file transfer details to receiving station...')
lostik.tx(packet.encode('ASCII').hex())

#listen for acknowledgement
lostik.await_ack()
print('Acknowledgement received.  Begin file transfer...')

for block in blocks:
    lostik.tx(block)
    current_block = blocks.index(block) + 1
    print(f'Sent block {current_block} of {len(blocks)}')
    sleep(.25)
    # lostik.await_ack()

#send OEF (end of file) message
lostik.tx('454F46')
print('DONE!')
print()
