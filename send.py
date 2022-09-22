########################################################################
#                                                                      #
#          NAME:  LMODEM - Send File                                   #
#  DEVELOPED BY:  Chris Clement (K7CTC)                                #
#       VERSION:  v0.4                                                 #
#                                                                      #
########################################################################

#import from project library
import lostik
from console import console

#import from standard library
import lzma
import textwrap
import argparse
from sys import exit
from hashlib import blake2b
from base64 import b85encode
from pathlib import Path

#import from 3rd party library
from rich.progress import Progress

#establish and parse command line arguments
parser = argparse.ArgumentParser(description='LMODEM - Send File',
                                 epilog='Created by K7CTC.')
parser.add_argument('outgoing_file',
                    help='filename to be sent')
parser.add_argument('-m', '--mode',
                    type=int,
                    choices=[1,2,3],
                    help='LMODEM starting mode (default: 1)',
                    default=1)
parser.add_argument('-c', '--channel',
                    type=int,
                    choices=[1,2,3],
                    help='LMODEM operating channel (default: 2)',
                    default=2)
args = parser.parse_args()
del parser

#set initial LoStik operating parameters
lostik.lmodem_set_mode(args.mode)
lostik.lmodem_set_channel(args.channel)

#check if outgoing file actually exists
if not Path(args.outgoing_file).is_file():
    print(f'[ERROR] {args.outgoing_file} does not exist in current working directory!')
    exit(1)

#LMODEM maximum file name length will henceforth be limited to 32 characters
if len(args.outgoing_file) > 32:
    print('[ERROR] File name exceeds 32 character limit!')
    print('HELP: Come on, this is LoRa we are working with here.')
    exit(1)

#get secure hash for outgoing file
with open(args.outgoing_file, 'rb') as file:
    outgoing_file_secure_hash = blake2b(digest_size=32)
    outgoing_file_secure_hash.update(file.read())

#compress outgoing file (in memory)
with open(args.outgoing_file, 'rb') as file:
    outgoing_file_compressed = lzma.compress(file.read())

#base85 encode compressed outgoing file
outgoing_file_compressed_b85 = b85encode(outgoing_file_compressed)

#LMODEM maximum OTA file size will henceforth be limited to 32kb
if len(outgoing_file_compressed_b85) > 32768:
    print('[ERROR] Compressed file exceeds maximum size of 32,768 bytes!')
    print('HELP: Come on, this is LoRa we are working with here.')
    exit(1)

#hex encode base85 encoded compressed outgoing file
outgoing_file_compressed_b85_hex = outgoing_file_compressed_b85.hex()

#split hex encoded base85 encoded compressed outgoing file into 128 byte blocks
blocks = textwrap.wrap(outgoing_file_compressed_b85_hex, 256)

#concatenate zero filled block index and block contents to create numbered packets
packets = []
for block in blocks:
    block_index_zfill = str(blocks.index(block)).zfill(3)
    block_index_zfill_hex = block_index_zfill.encode('ASCII').hex()
    packet = block_index_zfill_hex + block
    packets.append(packet)

total_air_time = 0
def send_requested_blocks(requested_block_number_list):
    global total_air_time
    with Progress() as progress:
        task = progress.
    
    
    for number in track(requested_block_number_list, description='Transferring...', auto_refresh=False):
    # for number in requested_block_number_list:
        time_sent, air_time = lostik.tx(packets[int(number)])
        total_air_time += air_time
    print()
    print()
    print('TX: All requested blocks sent.')
    lostik.tx('REQ_BLOCKS_SENT',encode=True)


# def send_requested_blocks(requested_block_number_list):
#     global total_air_time
#     for number in requested_block_number_list:
#         print(f'TX: Block {str(number).zfill(3)}', end='\r')
#         time_sent, air_time = lostik.tx(packets[int(number)])
#         total_air_time += air_time
#     print()
#     print()
#     print('TX: All requested blocks sent.')
#     lostik.tx('REQ_BLOCKS_SENT',encode=True)


#get size (on disk) of outgoing file
outgoing_file_size = Path(args.outgoing_file).stat().st_size
    
#show file transfer details
console.clear()
print('LMODEM v0.3 by Chris Clement (K7CTC)')
print()
print('File Transfer Details - Outgoing File')
print('-------------------------------------')
print(f'       Name: {args.outgoing_file}')
print(f'       Size: {outgoing_file_size} bytes (on disk) / {len(outgoing_file_compressed_b85)} bytes (over-the-air)')
print(f'Secure Hash: {outgoing_file_secure_hash.hexdigest()}')
print(f'     Blocks: {len(blocks)}')
print()

print(f'Communication mode: {lostik.lmodem_get_mode()}')
print(f'Communication channel: {lostik.lmodem_get_channel()}')
print()

# #basic handshake (listen for receive station ready)
# print('Connecting...')
# while True:
#     if lostik.rx(decode=True) == 'HANDSHAKE':
#         lostik.tx('HANDSHAKE', encode=True)
#         break
# print('Connected!')
# print()

#provide receiving station with the file transfer details
#file name | size on disk | size over the air | number of blocks to expect | secure hash
file_transfer_details = (args.outgoing_file + '|' +
                        str(outgoing_file_size) + '|' +
                        str(len(outgoing_file_compressed_b85)) + '|' +
                        str(len(blocks)) + '|' + 
                        outgoing_file_secure_hash.hexdigest())
print('TX: File transfer details.')
lostik.tx(file_transfer_details, encode=True)


requested_block_numbers_list = []
for packet in packets:
    requested_block_numbers_list.append(packets.index(packet))
send_requested_blocks(requested_block_numbers_list)







# #await initial reply
# reply = lostik.rx(decode=True)
# if reply == 'TIME-OUT':
#     print('[ERROR] LoStik watchdog timer time-out!')
#     exit(1)
# if reply == 'DUPLICATE_FILE':
#     print('RX: Duplicate file found and passed integrity check.')
#     print('ABORT!')
#     exit(0)
# if reply == 'DUPLICATE_FILENAME':
#     print('RX: Duplicate filename found.')
#     print('ABORT!')
#     exit(1)
# if reply[:3] == 'REQ':
#     print('RX: Ready to receive requested blocks.')
#     print()
#     requested_block_numbers_string = reply[3:]
#     requested_block_numbers_list = requested_block_numbers_string.split('|')
#     send_requested_blocks(requested_block_numbers_list)
# if reply == 'READY_TO_RECEIVE':
#     print('RX: Ready to receive file.')
#     print()
#     requested_block_numbers_list = []
#     for packet in packets:
#         requested_block_numbers_list.append(packets.index(packet))
#     send_requested_blocks(requested_block_numbers_list)

# #await reply after sending requested packets
# reply = lostik.rx(decode=True)
# if reply == 'TIME-OUT':
#     print('[ERROR] LoStik watchdog timer time-out!')
#     exit(1)
# if reply == 'INTEGRITY_PASS':
#     print('RX: File received and passed integrity check.')
#     print('DONE!')
#     exit(0)
# if reply == 'INTEGRITY_FAIL':
#     print('RX: File integrity check failed!')
#     print('[ERROR] Secure hash mismatch.  File integrity check failed!')
#     print('HELP: Please try again.')
#     exit(1)
# if reply == 'INCOMPLETE_TRANSFER':
#     print('RX: Partial file received.  Please try again.')
#     print('HELP: Try selecting a more robust LMODEM mode.')
#     exit(1)
