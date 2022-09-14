########################################################################
#                                                                      #
#          NAME:  LMODEM - Receive File                                #
#  DEVELOPED BY:  Chris Clement (K7CTC)                                #
#       VERSION:  v0.2                                                 #
#                                                                      #
########################################################################

#import from project library
from re import T
import lostik
from console import console

#import from standard library
import lzma
import os
import argparse
import json
from sys import exit
from hashlib import blake2b
from time import sleep
from base64 import b85decode
from pathlib import Path

#establish and parse command line arguments
parser = argparse.ArgumentParser(description='LMODEM - Receive File',
                                 epilog='Created by K7CTC.')
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

#set initial LoStik communication parameters
lostik.lmodem_set_mode(args.mode)
lostik.lmodem_set_channel(args.channel)

#basic handshake (tell sending station we are ready)
print('Connecting...', end='\r')
lostik.set_wdt('2500')
while True:
    lostik.tx('DTR', encode=True)
    if lostik.rx(decode=True) == 'DTR':
        break
print('Connected!   ')
lostik.set_wdt('5000')

#listen for incoming file details
incoming_file_details = lostik.rx(decode=True)
incoming_file_details_list = incoming_file_details.split('|')
incoming_file_name = incoming_file_details_list[0]
incoming_file_block_count = incoming_file_details_list[1]
incoming_file_secure_hash = incoming_file_details_list[2]
del incoming_file_details, incoming_file_details_list

#show file transfer details
console.clear()
print('File Transfer Details - Incoming File')
print('-------------------------------------')
print(f'       Name: {incoming_file_name}')
print(f'Secure Hash: {incoming_file_secure_hash}')
print(f'     Blocks: {incoming_file_block_count}')
print()

#check if incoming file already exists
if Path(incoming_file_name).is_file():
    #and check integrity if it does
    with open(incoming_file_name, 'rb') as file:
        local_file_secure_hash = blake2b(digest_size=32)
        local_file_secure_hash.update(file.read())
    if incoming_file_secure_hash == local_file_secure_hash.hexdigest():
        print('Identical file already exists in current directory.')
        print('DONE!')
        lostik.tx('DUP', encode=True)
        exit(0)
    if incoming_file_secure_hash != local_file_secure_hash.hexdigest():
        print(f'[ERROR] {incoming_file_name} already exists in current directory')
        print('though it failed the integrity check against the incoming file.')
        print('HELP: Please delete or rename the existing file and try again.')
        lostik.tx('CAN', encode=True)
        exit(1)

#function to place received blocks into dictionary
def receive_incoming_blocks():
    while True:           
        incoming_packet = lostik.rx()
        if incoming_packet == '534E54' or incoming_packet == 'TOT':
            break
        incoming_block_number_hex = incoming_packet[:6]
        incoming_block_number_ascii = bytes.fromhex(incoming_block_number_hex).decode('ASCII')
        incoming_block_number_int = int(incoming_block_number_ascii)
        incoming_block = incoming_packet[6:]
        #received_blocks[incoming_block_number_int] = incoming_block
        received_blocks.update({incoming_block_number_int: incoming_block})
        print(f'Received Block: {str(incoming_block_number_int).zfill(3)}')

#resume partial transfer or begin new transfer
partial_file = incoming_file_name + '.json'
if Path(partial_file).is_file():
    with open(partial_file) as json_file:
        received_blocks = json.load(json_file)
    os.remove(partial_file)
    print(received_blocks)
    input()
    if incoming_file_secure_hash == received_blocks['secure_hash']:
        received_blocks.pop('secure_hash')
        print('Partial file found.  Resuming file transfer...')
        missing_blocks = ''
        for block in received_blocks:
            if received_blocks[block] == '':
                missing_blocks = missing_blocks + str(block) + '|'
        missing_blocks = missing_blocks[:-1]
        packet = 'REQ' + missing_blocks
        lostik.tx(packet, encode=True)
        receive_incoming_blocks()
else:
    received_blocks = {block: '' for block in range(int(incoming_file_block_count))}
    lostik.tx('RTR', encode=True)
    receive_incoming_blocks()


# print(received_blocks)
# input()


#check for missing blocks
missing_blocks = ''
for block in received_blocks:
    if received_blocks[block] == '':
        missing_blocks = missing_blocks + str(block) + '|'

#if all blocks received, process file
if len(missing_blocks) == 0:
    print('All file blocks received.  Processing file...')
    #write completed file to disk and check integrity
    output_file_compressed_b85_hex = ''
    for block in received_blocks.values():
        output_file_compressed_b85_hex = output_file_compressed_b85_hex + block
    #decode from hex
    output_file_compressed_b85 = bytes.fromhex(output_file_compressed_b85_hex)
    #decode from b85
    output_file_compressed = b85decode(output_file_compressed_b85)
    #decompress
    output_file = lzma.decompress(output_file_compressed)
    #write to disk
    with open(incoming_file_name, 'wb') as file:
        file.write(output_file)
    #obtain secure hash for received file
    with open(incoming_file_name, 'rb') as file:
        output_file_secure_hash = blake2b(digest_size=32)
        output_file_secure_hash.update(file.read())
    if incoming_file_secure_hash != output_file_secure_hash.hexdigest():
        print('[ERROR] Secure has mismatch.  File integrity check failed!')
        os.remove(incoming_file_name)
        lostik.tx('CAN', encode=True)
        exit(1)
    if incoming_file_secure_hash == output_file_secure_hash.hexdigest():
        print('File integrity check PASSED!  File transfer complete.')
        lostik.tx('FIN', encode=True)
        exit(0)

#if some blocks missing, write partial file and exit
if len(missing_blocks) != 0:
    print('File transfer incomplete.  Writing partial file to disk.')
    received_blocks['secure_hash'] = incoming_file_secure_hash
    with open(partial_file, 'w') as json_file:
        json.dump(received_blocks, json_file)
    lostik.tx('CAN', encode=True)
    exit(1)
