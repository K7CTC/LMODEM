########################################################################
#                                                                      #
#          NAME:  LMODEM - Receive File                                #
#  DEVELOPED BY:  Chris Clement (K7CTC)                                #
#       VERSION:  v0.4                                                 #
#                                                                      #
########################################################################

#standard library imports
import lzma
import os
import argparse
import json
from sys import exit
from hashlib import blake2b
from base64 import b85decode
from pathlib import Path

#related third party imports
from rich.progress import progress

#local application/library specific imports
import lostik
import ui
from console import console

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

#display the user interface
ui.print_static_content()

#set initial LoStik communication parameters
lostik.lmodem_set_mode(args.mode)
lostik.lmodem_set_channel(args.channel)

#update the user interface
ui.insert_module_version('v0.4')
ui.insert_module_name('Receive File')
ui.insert_lmodem_channel(lostik.lmodem_get_channel())
ui.insert_lmodem_mode(lostik.lmodem_get_mode())
ui.insert_frequency(lostik.get_freq())
ui.insert_bandwidth(lostik.get_bw())
ui.insert_power(lostik.get_pwr())
ui.insert_spreading_factor(lostik.get_sf())
ui.insert_coding_rate(lostik.get_cr())

#handshake (tell sending station we are ready)
ui.update_status('Connecting...')
# while True:
#     lostik.tx('HANDSHAKE', encode=True)
#     if lostik.rx(decode=True) == 'HANDSHAKE':
#         break
ui.update_status('Connected!')

#listen for incoming file details
ui.update_status('Awaiting file transfer details.')
file_transfer_details = lostik.rx(decode=True)
if file_transfer_details == 'TIME-OUT':
    ui.update_status('[red1 on deep_sky_blue4][ERROR][/] LoStik watchdog timer time-out!')
    exit(1)
else:    
    file_transfer_details_list = file_transfer_details.split('|')
    incoming_file_name = file_transfer_details_list[0]
    incoming_file_size = file_transfer_details_list[1]
    incoming_file_size_ota = file_transfer_details_list[2]
    incoming_file_block_count = file_transfer_details_list[3]
    incoming_file_secure_hash = file_transfer_details_list[4]
    del file_transfer_details, file_transfer_details_list

#show file transfer details
ui.update_status('Received file transfer details.')
ui.insert_file_name(incoming_file_name)
ui.insert_file_size(incoming_file_size)
ui.insert_file_size_ota(incoming_file_size_ota)
ui.insert_secure_hash(incoming_file_secure_hash)
ui.insert_blocks(incoming_file_block_count)

#check if incoming file already exists
if Path(incoming_file_name).is_file():
    #and check integrity if it does
    with open(incoming_file_name, 'rb') as file:
        local_file_secure_hash = blake2b(digest_size=16)
        local_file_secure_hash.update(file.read())
    if incoming_file_secure_hash == local_file_secure_hash.hexdigest():
        ui.update_status('[green1 on deep_sky_blue4][DONE][/] Duplicate file found. Integrity check passed.')
        lostik.tx('DUPLICATE_PASS', encode=True)
        exit(0)
    if incoming_file_secure_hash != local_file_secure_hash.hexdigest():
        ui.update_status('[red1 on deep_sky_blue4][ERROR][/] Duplicate filename found. Integrity check failed!')
        lostik.tx('DUPLICATE_FAIL', encode=True)
        exit(1)

received_blocks = {}

#function to place received blocks into dictionary
def receive_requested_blocks():
    time_out_counter = 0
    while True:           
        incoming_packet = lostik.rx()
        if incoming_packet == '5245515F424C4F434B535F53454E54':
            print()
            print()
            print('RX: All requested blocks sent.')
            print()
            break
        if incoming_packet == 'TIME-OUT':
            print()
            print()
            print('[ERROR] LoStik watchdog timer time-out!')
            print()
            time_out_counter += 1
            if time_out_counter == 3:
                break
            continue
        incoming_block_number_hex = incoming_packet[:6]
        incoming_block_number = bytes.fromhex(incoming_block_number_hex).decode('ASCII')
        incoming_block = incoming_packet[6:]
        received_blocks.update({incoming_block_number: incoming_block})
        print(f'RX: Block {incoming_block_number}', end='\r')
    

#function to return a string of pipe delimited missing block numbers, if any
def create_missing_blocks_string(received_blocks):
    missing_blocks_string = ''
    for block in received_blocks:
        if received_blocks[block] == '':
            missing_blocks_string = missing_blocks_string + str(block) + '|'
    if len(missing_blocks_string) != 0:
        missing_blocks_string = missing_blocks_string[:-1]
    return missing_blocks_string

def received_block_count(received_blocks):
    number_of_received_blocks = 0
    for block in received_blocks:
        if received_blocks[block] != '':
            received_block_count += 1
    return receive


#resume partial transfer or begin new transfer
partial_file = incoming_file_name + '.json'
if Path(partial_file).is_file():
    with open(partial_file) as json_file:
        received_blocks = json.load(json_file)
    os.remove(partial_file)
    if incoming_file_secure_hash == received_blocks['secure_hash']:
        received_blocks.pop('secure_hash')
        print('Partial file found.  Resuming file transfer...')
        missing_blocks = create_missing_blocks_string(received_blocks)
        if len(missing_blocks) > 123: #to ensure our outgoing packet does not exceed 128 bytes
            missing_blocks = missing_blocks[:123]
        requested_block_numbers = 'REQ' + missing_blocks
        print('TX: Ready to receive requested blocks.')
        print()
        lostik.tx(requested_block_numbers, encode=True)
        receive_requested_blocks()
else:
    print('TX: Ready to receive file.')
    print()
    keys = []
    for i in range(int(incoming_file_block_count)):
        keys.append(str(i).zfill(3))
    received_blocks = dict.fromkeys(keys, '')
    lostik.tx('READY_TO_RECEIVE', encode=True)
    receive_requested_blocks()

missing_blocks = create_missing_blocks_string(received_blocks)

#if all blocks received, process file
if missing_blocks == '':
    print('All file blocks received.  Processing file...')
    print()
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
        output_file_secure_hash = blake2b(digest_size=16)
        output_file_secure_hash.update(file.read())
    if incoming_file_secure_hash != output_file_secure_hash.hexdigest():
        print('[ERROR] Secure hash mismatch.  File integrity check failed!')
        print('HELP: Please try again.')
        print('TX: File integrity check failed!')        
        os.remove(incoming_file_name)
        lostik.tx('INTEGRITY_FAIL', encode=True)
        exit(1)
    if incoming_file_secure_hash == output_file_secure_hash.hexdigest():
        print('TX: File received and passed integrity check.')
        print('DONE!')
        lostik.tx('INTEGRITY_PASS', encode=True)
        exit(0)
#if some blocks missing, write partial file to disk
else:
    print('File transfer incomplete.  Writing partial file to disk.')
    received_blocks['secure_hash'] = incoming_file_secure_hash
    with open(partial_file, 'w') as json_file:
        json.dump(received_blocks, json_file, indent=4)
    print('TX: Partial file received.  Please try again.')
    print('HELP: Try selecting a mode robust LMODEM mode.')
    lostik.tx('INCOMPLETE_TRANSFER', encode=True)
    exit(1)
