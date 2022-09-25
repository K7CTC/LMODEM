########################################################################
#                                                                      #
#          NAME:  LMODEM - Send File                                   #
#  DEVELOPED BY:  Chris Clement (K7CTC)                                #
#       VERSION:  v0.4                                                 #
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

from time import sleep

#related third party imports
import rich.progress

#local application/library specific imports
import lostik
import ui

#establish and parse command line arguments
parser = argparse.ArgumentParser(description='LMODEM - Send File',
                                 epilog='Created by Chris Clement (K7CTC).')
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

#display the user interface
ui.print_static_content()

#set initial LoStik operating parameters
lostik.lmodem_set_mode(args.mode)
lostik.lmodem_set_channel(args.channel)

#update the user interface
ui.insert_module_version('v0.4')
ui.insert_module_name('Send File')
ui.insert_frequency(lostik.get_freq())
ui.insert_bandwidth(lostik.get_bw())
ui.insert_power(lostik.get_pwr())
ui.insert_spreading_factor(lostik.get_sf())
ui.insert_coding_rate(lostik.get_cr())
ui.insert_lmodem_mode(lostik.lmodem_get_mode())
ui.insert_lmodem_channel(lostik.lmodem_get_channel())
ui.insert_file_name(args.outgoing_file)

#check if outgoing file actually exists
if not Path(args.outgoing_file).is_file():
    ui.update_status('[ERROR] File does not exist!')
    exit(1)

#LMODEM maximum file name length will henceforth be limited to 32 characters
if len(args.outgoing_file) > 32:
    ui.update_status('[ERROR] File name exceeds 32 character limit!')
    exit(1)

#get secure hash for outgoing file
with open(args.outgoing_file, 'rb') as file:
    outgoing_file_secure_hash = blake2b(digest_size=16)
    outgoing_file_secure_hash.update(file.read())
ui.insert_secure_hash(outgoing_file_secure_hash.hexdigest())

#compress outgoing file (in memory)
with open(args.outgoing_file, 'rb') as file:
    outgoing_file_compressed = lzma.compress(file.read())

#base85 encode compressed outgoing file
outgoing_file_compressed_b85 = b85encode(outgoing_file_compressed)
ui.insert_file_size_ota(len(outgoing_file_compressed_b85))

#LMODEM maximum OTA file size will henceforth be limited to 32kb
if len(outgoing_file_compressed_b85) > 32768:
    ui.update_status('[ERROR] Compressed file exceeds maximum size of 32,768 bytes!')
    exit(1)

#hex encode base85 encoded compressed outgoing file
outgoing_file_compressed_b85_hex = outgoing_file_compressed_b85.hex()

#split hex encoded base85 encoded compressed outgoing file into 128 byte blocks
blocks = textwrap.wrap(outgoing_file_compressed_b85_hex, 256)
ui.insert_blocks(len(blocks))

#get size (on disk) of outgoing file
outgoing_file_size = Path(args.outgoing_file).stat().st_size
ui.insert_file_size(outgoing_file_size)

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
    ui.update_status('Sending requested blocks.')
    ui.move_cursor(21,1)
    progress = rich.progress.Progress(rich.progress.BarColumn(bar_width=None),
                                      rich.progress.TaskProgressColumn(),
                                      rich.progress.TimeRemainingColumn(),
                                      rich.progress.TimeElapsedColumn(),
                                      expand=True)
    with progress:
        for number in progress.track(requested_block_number_list):
            time_sent, air_time = lostik.tx(packets[int(number)])
            total_air_time += air_time
    ui.update_status('All requested blocks sent.')
    lostik.tx('REQ_BLOCKS_SENT',encode=True)

#new handshake
ui.update_status('Connecting...')
# while True:
#     if lostik.rx(decode=True) == 'HANDSHAKE':
#         lostik.tx('HANDSHAKE', encode=True)
#         break

sleep(4)
ui.update_status('Connected!')




#provide receiving station with the file transfer details
#file name | size on disk | size over the air | number of blocks to expect | secure hash
file_transfer_details = (args.outgoing_file + '|' +
                        str(outgoing_file_size) + '|' +
                        str(len(outgoing_file_compressed_b85)) + '|' +
                        str(len(blocks)) + '|' + 
                        outgoing_file_secure_hash.hexdigest())
ui.update_status('Sending file transfer details...')
lostik.tx(file_transfer_details, encode=True)
ui.update_status('File trandfer details sent.')


#testing code
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
