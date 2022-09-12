########################################################################
#                                                                      #
#          NAME:  LMODEM - Receive File                                #
#  DEVELOPED BY:  Chris Clement (K7CTC)                                #
#       VERSION:  v0.2                                                 #
#                                                                      #
########################################################################

#import from project library
import lostik
from console import console

#import from standard library
import lzma
import os
from sys import exit
from hashlib import blake2b
from time import sleep
from base64 import b85decode

#set LMODEM mode to 1
lostik.lmodem_set_mode(1)

#set LMODEM channel to 2 (915 MHz)
lostik.lmodem_set_channel(2)

#handshake (actively beacon to sending station that we are ready)
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
incoming_file_blocks = incoming_file_details_list[1]
incoming_file_secure_hash = incoming_file_details_list[2]
del incoming_file_details, incoming_file_details_list

#show file transfer details
console.clear()
print('File Transfer Details - Incoming File')
print('-------------------------------------')
print(f'       Name: {incoming_file_name}')
print(f'Secure Hash: {incoming_file_secure_hash}')
print(f'     Blocks: {incoming_file_blocks}')

#create dictionary to store received blocks
received_blocks = {block: '' for block in range(int(incoming_file_blocks))}

#send ready to receive packet
lostik.tx('RTR', encode=True)

#receive incoming file
while True:
    incoming_packet = lostik.rx()
    if incoming_packet == '454E44' or incoming_packet == 'TOT':
        break
    incoming_block_number_hex = incoming_packet[:6]
    incoming_block_number_ascii = bytes.fromhex(incoming_block_number_hex).decode('ASCII')
    incoming_block_number_int = int(incoming_block_number_ascii)
    incoming_block = incoming_packet[6:]
    received_blocks[incoming_block_number_int] = incoming_block
    print(f'Received block {str(incoming_block_number_int).zfill(3)} of {str(incoming_file_blocks).zfill(3)}', end='\r')

# #mess with the data to test resend feature
# received_blocks[3] = ''
# received_blocks[6] = ''
# received_blocks[9] = ''

#check for missing blocks
missing_blocks = ''
for block in received_blocks:
    if received_blocks[block] == '':
        missing_blocks = missing_blocks + str(block) + '|'


if len(missing_blocks) == 0:
    # REBUILD FILE ON THE "OTHER END"
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

    print(f'Incoming File Secure Hash: {incoming_file_secure_hash}')
    print(f'  Output File Secure Hash: {output_file_secure_hash.hexdigest()}')

    if incoming_file_secure_hash != output_file_secure_hash.hexdigest():
        print('[ERROR] Secure has mismatch.  File integrity check failed!')
        os.remove(incoming_file_name)
        exit(1)

    print('File integrity check PASSED!  File transfer complete.')
    lostik.tx('ACK', encode=True)
    lostik.tx('ACK', encode=True)
    lostik.tx('ACK', encode=True)

    exit(0)



if len(missing_blocks) != 0:
    missing_blocks = missing_blocks[:-1]
    packet = 'NAK' + missing_blocks
    print(packet)
    sleep(1)
    lostik.tx(packet, encode=True)

#get missing packets

