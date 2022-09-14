########################################################################
#                                                                      #
#          NAME:  LMODEM - Send File                                   #
#  DEVELOPED BY:  Chris Clement (K7CTC)                                #
#       VERSION:  v0.2                                                 #
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
from time import sleep
from base64 import b85encode
from pathlib import Path

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
def send_requested_packets(packet_number_list):
    global total_air_time
    for number in packet_number_list:
        print(f'Sending Block: {str(number).zfill(3)}')
        time_sent, air_time = lostik.tx(packets[int(number)])
        print(f'Air Time: {air_time}')
        total_air_time += air_time
    lostik.tx('SNT',encode=True)

#get size (on disk) of outgoing file
outgoing_file_size = Path(args.outgoing_file).stat().st_size
    
#show file transfer details
console.clear()
print('File Transfer Details - Outgoing File')
print('-------------------------------------')
print(f'       Name: {args.outgoing_file}')
print(f'       Size: {outgoing_file_size} bytes (on disk) / {len(outgoing_file_compressed_b85)} bytes (over-the-air)')
print(f'Secure Hash: {outgoing_file_secure_hash.hexdigest()}')
print(f'     Blocks: {len(blocks)}')
print()

print(f'Selected communication mode: {lostik.lmodem_get_mode()}')
print(f'Selected communication channel: {lostik.lmodem_get_channel()}')
print()

#basic handshake (listen for receive station ready)
print('Connecting...')
while True:
    if lostik.rx(decode=True) == 'DTR':
        lostik.tx('DTR', encode=True)
        break
print('Connected!')













#provide receiving station with the file transfer details
#file name | number of blocks to expect | secure hash
packet = args.outgoing_file + '|' + str(len(blocks)) + '|' + outgoing_file_secure_hash.hexdigest()
lostik.tx(packet, encode=True)
print('File transfer details sent...')
del packet

#await initial reply
reply = lostik.rx(decode=True)
if reply[:3] == 'TOT':
    print('[ERROR] LoStik watchdog timer time-out!')
    exit(1)
if reply[:3] == 'DUP':
    print('File already exists at receiving station.')
    print('DONE!')
    exit(0)
if reply[:3] == 'CAN':
    print('Receiving station has cancelled the file transfer.')
    print('DONE!')
    exit(0)
if reply[:3] == 'REQ':
    print('Receiving station has partial file.  Resuming file transfer...')
    requested_packet_numbers_string = reply[3:]
    requested_packet_numbers_list = requested_packet_numbers_string.split('|')
    send_requested_packets(requested_packet_numbers_list)
if reply[:3] == 'RTR':
    print('Receive station is ready, sending file...')
    requested_packet_numbers_list = []
    for packet in packets:
        requested_packet_numbers_list.append(packets.index(packet))
    send_requested_packets(requested_packet_numbers_list)









#await reply after sending requested packets
reply = lostik.rx(decode=True)
if reply[:3] == 'TOT':
    print('[ERROR] LoStik watchdog timer time-out!')
    exit(1)
if reply[:3] == 'CAN':
    print('Receiving station has cancelled the file transfer.')
    print('DONE!')
    exit(0)
if reply[:3] == 'FIN':
    print('Receive station reports file transfer successful.')
    print('DONE!')
    exit(0)

    

# if reply[:3] == 'NAK':
#     print('Receiving station has partial file.  Resuming file transfer...')
#     requested_packet_numbers_string = reply[3:]
#     requested_packet_numbers_list = requested_packet_numbers_string.split('|')
#     send_requested_packets(requested_packet_numbers_list)
















# #await ready to receive
# if lostik.rx(decode=True) == 'RTR':
#     print('Receive station ready.  Sending File...')
#     send_file()
#     print('File sent.')

# #await ACK or NAK
# print('Await...')
# reply = lostik.rx(decode=True)

# if reply[:3] == 'ACK':
#     print('File transfer successful!')
#     exit(0)
# if reply[:3] == 'TOT':
#     print('Time-out!')
#     exit(1)
# if reply[:3] == 'NAK':
#     missing_packet_numbers_string = reply[3:]
#     console.print(f'Missing Packet Numbers: {missing_packet_numbers_string}')
#     missing_packet_numbers_list = missing_packet_numbers_string.split('|')
#     send_missing_packets(missing_packet_numbers_list)
#     print('Missing packets sent.')

# #await final ACK or NAK
# reply = lostik.rx(decode=True)
# if reply[:3] == 'ACK':
#     print('File transfer successful!')
#     exit(0)
# if reply[:3] == 'TOT':
#     print('Time-out!')
#     exit(1)
# if reply[:3] == 'NAK':
#     print('File transfer failed!  Please try again.')
#     exit(1)























# total_air_time = 0

# def send_file():
#     global total_air_time
#     for packet in outgoing_packets:
#         time_sent, air_time = lostik.tx(packet)
#         total_air_time += air_time
#         sent_packet_number = outgoing_packets.index(packet) + 1
#         print(f'Sent block {str(sent_packet_number).zfill(3)} of {str(len(outgoing_packets)).zfill(3)} (air time: {str(air_time).zfill(3)}  total air time: {str(total_air_time).zfill(4)})', end='\r')
#         # sleep(.15)
#     #send end of file message 3x
#     print()
#     for i in range(3):
#         lostik.tx('END',encode=True)
#         sleep(.15)

# def send_missing_packets(missing_packet_numbers):
#     global total_air_time
#     lostik.lmodem_set_mode(3)
#     for number in missing_packet_numbers:
#         time_sent, air_time = lostik.tx(outgoing_packets[int(number)])
#         #print(outgoing_packets[int(number)])
#         total_air_time += air_time
#         print('Sending Missing Block...')
#         # sleep(.15)
#     #send end of file message 3x
#     for i in range(3):
#         lostik.tx('FIN',encode=True)
#         sleep(.15)
