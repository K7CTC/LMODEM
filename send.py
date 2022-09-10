########################################################################
#                                                                      #
#          NAME:  LMODEM - Send File                                   #
#  DEVELOPED BY:  Chris Clement (K7CTC)                                #
#       VERSION:  v0.2                                                 #
#                                                                      #
########################################################################

#import from project library
import re
import lostik
import lostik_settings
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
outgoing_blocks = textwrap.wrap(outgoing_file_compressed_b85_hex, 256)

#concatenate zero filled block number and block contents to create numbered packets
outgoing_packets = []
for block in outgoing_blocks:
    block_index_zfill = str(outgoing_blocks.index(block)).zfill(3)
    block_index_zfill_hex = block_index_zfill.encode('ASCII').hex()
    packet = block_index_zfill_hex + block
    outgoing_packets.append(packet)
del outgoing_blocks

#show file transfer details
console.clear()
print('File Transfer Details - Outgoing File')
print('-------------------------------------')
print(f'       Name: {args.outgoing_file}')
print(f'       Size: {outgoing_file_size} bytes (on disk) / {len(outgoing_file_compressed_b85)} bytes (over-the-air)')
print(f'Secure Hash: {outgoing_file_secure_hash.hexdigest()}')
print(f'     Blocks: {len(outgoing_packets)}')
print()

#handshake
print('Connecting...')
lostik.set_wdt('2000')
while True:
    lostik.tx('DTR', encode=True)
    if lostik.rx(decode=True) == 'DTR':
        break
print('Connected!   ')
print()
lostik.set_wdt(lostik_settings.WDT)
sleep(.5)

# provide receiving station with the file transfer details
# file name | number of blocks to expect | secure hash
packet = args.outgoing_file + '|' + str(len(outgoing_packets)) + '|' + outgoing_file_secure_hash.hexdigest()
lostik.tx(packet, encode=True)
print('File transfer details sent...')
del packet

#total air time needs to be global so we can calculare resent packets as well

def send_file():
    total_air_time = 0
    for packet in outgoing_packets:
        time_sent, air_time = lostik.tx(packet)
        total_air_time += air_time
        sent_packet_number = outgoing_packets.index(packet) + 1
        print(f'Sent block {str(sent_packet_number).zfill(3)} of {str(len(outgoing_packets)).zfill(3)} (air time: {str(air_time).zfill(3)}  total air time: {str(total_air_time).zfill(4)})', end='\r')
        # sleep(.15)
    #send end of file message 3x
    for i in range(3):
        lostik.tx('END',encode=True)
        sleep(.15)

def send_missing_packets(missing_packets):
    for packet in missing_packets:
        time_sent, air_time = lostik.tx(packet)
        total_air_time += air_time
        sent_packet_number = outgoing_packets.index(packet) + 1
        print(f'Sent block {str(sent_packet_number).zfill(3)} of {str(len(outgoing_packets)).zfill(3)} (air time: {str(air_time).zfill(3)}  total air time: {str(total_air_time).zfill(4)})', end='\r')
        sleep(.15)
    #send end of file message 3x
    for i in range(3):
        lostik.tx('FIN',encode=True)
        sleep(.15)

#await ready to receive
if lostik.rx(decode=True) == 'RTR':
    print('Receive station ready.  Sending File...')
    print()
    send_file()
    
#await ACK or NAK
reply = lostik.rx(decode=True)
print(reply)


if reply[:3] == 'ACK':
    print('File transfer successful!')
    exit(0)
if reply[:3] == 'TOT':
    print('Time-out!')
    exit(1)
if reply[:3] == 'NAK':
    missing_packets_string = reply[3:]
    console.print(missing_packets_string)
    missing_packets_list = missing_packets_string.split('|')
    console.print(missing_packets_list)

    input('INPUT')
    for packet in missing_packets_list:
        print(packet)

    input()


    send_missing_packets(missing_packets_list)

#await final ACK or NAK
reply = lostik.rx(decode=True)
if reply[:3] == 'ACK':
    print('File transfer successful!')
    exit(0)
if reply[:3] == 'TOT':
    print('Time-out!')
    exit(1)
if reply[:3] == 'NAK':
    print('File transfer failed!  Please try again.')
    exit(1)
