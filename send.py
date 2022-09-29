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
ui.insert_lmodem_channel(lostik.lmodem_get_channel())
ui.insert_lmodem_mode(lostik.lmodem_get_mode())
ui.insert_frequency(lostik.get_freq())
ui.insert_bandwidth(lostik.get_bw())
ui.insert_power(lostik.get_pwr())
ui.insert_spreading_factor(lostik.get_sf())
ui.insert_coding_rate(lostik.get_cr())
ui.insert_file_name(args.outgoing_file)

#check if outgoing file actually exists
if not Path(args.outgoing_file).is_file():
    ui.update_status('[red1 on deep_sky_blue4][ERROR][/] File does not exist!')
    exit(1)

#check if outgoing filename exceeds LMODEM maximum length of 32 characters
if len(args.outgoing_file) > 32:
    ui.update_status('[red1 on deep_sky_blue4][ERROR][/] File name exceeds 32 character limit!')
    exit(1)

#generate secure hash hex digest for outgoing file
with open(args.outgoing_file, 'rb') as file:
    outgoing_file_secure_hash = blake2b(digest_size=16)
    outgoing_file_secure_hash.update(file.read())
    outgoing_file_secure_hash_hex_digest = outgoing_file_secure_hash.hexdigest()

del outgoing_file_secure_hash

ui.insert_secure_hash(outgoing_file_secure_hash_hex_digest)

#compress outgoing file (in memory) using lzma algorithm
with open(args.outgoing_file, 'rb') as file:
    outgoing_file_compressed = lzma.compress(file.read())

#base85 encode compressed outgoing file
outgoing_file_compressed_b85 = b85encode(outgoing_file_compressed)

del outgoing_file_compressed

#determine over-the-air outgoing file size in bytes
outgoing_file_size_ota = len(outgoing_file_compressed_b85)

ui.insert_file_size_ota(outgoing_file_size_ota)

#check if outgoing file size over-the-air exceeds LMODEM maximum of 32768 bytes
if outgoing_file_size_ota > 32768:
    ui.update_status('[red1 on deep_sky_blue4][ERROR][/] Size (over the air) exceeds maximum of 32768 bytes!')
    exit(1)

#determine on disk outgoing file size in bytes
outgoing_file_size_on_disk = Path(args.outgoing_file).stat().st_size

ui.insert_file_size_on_disk(outgoing_file_size_on_disk)

#hex encode base85 encoded compressed outgoing file
outgoing_file_compressed_b85_hex = outgoing_file_compressed_b85.hex()

del outgoing_file_compressed_b85

#split hex encoded base85 encoded compressed outgoing file into 128 byte blocks
blocks = textwrap.wrap(outgoing_file_compressed_b85_hex, 256)

del outgoing_file_compressed_b85_hex

block_count = len(blocks)

ui.insert_block_count(block_count)

#concatenate zero filled block index and block contents to create numbered packets
packets = []
for block in blocks:
    block_index_zfill = str(blocks.index(block)).zfill(3)
    block_index_zfill_hex = block_index_zfill.encode('ASCII').hex()
    packet = block_index_zfill_hex + block
    packets.append(packet)
del blocks

def send_requested_blocks(received_block_count, requested_blocks):
    global block_count
    ui.update_status('Transmitting requested blocks.')
    ui.move_cursor(21,1)
    progress = rich.progress.Progress(rich.progress.BarColumn(bar_width=59),
                                      rich.progress.TaskProgressColumn(),
                                      rich.progress.TimeRemainingColumn(),
                                      rich.progress.TimeElapsedColumn())
    task = progress.add_task('Send Requested Blocks', total=block_count)
    with progress:
        sent_block_count = 0    
        progress.update(task, completed=received_block_count+sent_block_count)
        for block_number in requested_blocks:
            lostik.tx(packets[int(block_number)], delay=.15)
            sent_block_count += 1
            progress.update(task, completed=received_block_count+sent_block_count)
    lostik.tx('REQ_BLOCKS_SENT', encode=True)
    ui.update_status('All requested blocks sent.')

#handshake
ui.update_status('Connecting...')
while True:
    if lostik.rx(decode=True) == 'HANDSHAKE':
        lostik.tx('HANDSHAKE', encode=True)
        break
ui.update_status('Connected!')

#provide receiving station with the file transfer details
#file name | size on disk | size over the air | number of blocks | secure hash
file_transfer_details = (args.outgoing_file + '|' +
                        str(outgoing_file_size_on_disk) + '|' +
                        str(outgoing_file_size_ota) + '|' +
                        str(block_count) + '|' + 
                        outgoing_file_secure_hash_hex_digest)
del outgoing_file_size_on_disk, outgoing_file_size_ota, block_count, outgoing_file_secure_hash_hex_digest
ui.update_status('Transmitting file transfer details.')
lostik.tx(file_transfer_details, encode=True)
ui.update_status('File transfer details sent.')

#await initial reply
ui.update_status('Awaiting instruction from receive station.')
reply = lostik.rx(decode=True)
if reply == 'TIME-OUT':
    ui.update_status('[red1 on deep_sky_blue4][ERROR][/] LoStik watchdog timer time-out!')
    exit(1)
elif reply == 'DUPLICATE_PASS':
    ui.update_status('[green1 on deep_sky_blue4][DONE][/] Duplicate file found. Integrity check passed.')
    exit(0)
elif reply == 'DUPLICATE_FAIL':
    ui.update_status('[red1 on deep_sky_blue4][ERROR][/] Duplicate filename found. Integrity check failed!')
    exit(1)
else:
    received_block_count = int(reply[:3])
    if received_block_count == 0:
        ui.update_status('Starting file transfer.')
        requested_blocks = []
        for packet in packets:
            requested_blocks.append(packets.index(packet))
        requested_block_count = len(requested_blocks)
        ui.insert_requested_block_count(requested_block_count)
        del requested_block_count
        send_requested_blocks(received_block_count, requested_blocks)
        del requested_blocks
    else:
        ui.update_status('Resuming file transfer.')
        requested_block_numbers = reply[3:]
        requested_blocks = requested_block_numbers.split('|')
        requested_block_count = len(requested_blocks)
        ui.insert_requested_block_count(requested_block_count)
        del requested_block_count
        send_requested_blocks(received_block_count, requested_blocks)
        del requested_blocks



# if reply == 'READY_TO_RECEIVE':
#     ui.update_status('Starting file transfer.')
#     requested_blocks = []
#     for packet in packets:
#         requested_blocks.append(packets.index(packet))
#     requested_block_count = len(requested_blocks)
#     ui.insert_requested_block_count(requested_block_count)
#     del requested_block_count
#     send_requested_blocks(requested_blocks)
#     del requested_blocks
# if reply[:3] == 'REQ':
#     ui.update_status('Resuming file transfer.')
#     requested_block_numbers = reply[3:]
#     requested_blocks = requested_block_numbers.split('|')
#     requested_block_count = len(requested_blocks)
#     ui.insert_requested_block_count(requested_block_count)
#     del requested_block_count
#     send_requested_blocks(requested_blocks)
#     del requested_blocks
    


#await reply after sending requested packets
ui.update_status('Awaiting transfer result from receive station.')
reply = lostik.rx(decode=True)
if reply == 'TIME-OUT':
    ui.update_status('[red1 on deep_sky_blue4][ERROR][/] LoStik watchdog timer time-out!')
    exit(1)
if reply == 'INCOMPLETE':
    ui.update_status('[orange1 on deep_sky_blue4][WARNING][/] File transfer incomplete. Try again to resume.')
    exit(1)
if reply == 'COMPLETE_FAIL':
    ui.update_status('[red1 on deep_sky_blue4][ERROR][/] File transfer complete. Integrity check failed!')
    exit(1)
if reply == 'COMPLETE_PASS':
    ui.update_status('[green1 on deep_sky_blue4][DONE][/] File transfer complete. Integrity check passed.')
    exit(0)
