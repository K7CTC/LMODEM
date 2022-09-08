########################################################################
#                                                                      #
#          NAME:  LMODEM - Receive                                     #
#  DEVELOPED BY:  Chris Clement (K7CTC)                                #
#       VERSION:  v0.2                                                 #
#                                                                      #
########################################################################

#import from project library
from console import console
import lostik

#import from standard library
from sys import exit
from time import sleep
from hashlib import blake2b
from base64 import b85decode
import os
import lzma
import base64

#listen for incoming file details
lostik.set_wdt('300000') #five minutes
print('Listening...')
incoming_file_details = lostik.rx(decode=True)
incoming_file_details_list = incoming_file_details.split('|')
incoming_file_name = incoming_file_details_list[0]
incoming_file_blocks = incoming_file_details_list[1]
incoming_file_secure_hash = incoming_file_details_list[2]
del incoming_file_details, incoming_file_details_list

console.clear()
print('File Transfer Details - Incoming File')
print('-------------------------------------')
print(f'       Name: {incoming_file_name}')
print(f'Secure Hash: {incoming_file_secure_hash}')
print(f'     Blocks: {incoming_file_blocks}')

received_blocks = {block: '' for block in range(incoming_file_blocks)}


print(received_blocks)



# #send READY
# lostik.tx('READY', encode = True)


# #get file
# received_hex_string_compressed = ''
# while True:
#     lostik.rx(True)
#     rx_payload = ''
#     while rx_payload == '':
#         rx_payload = lostik.read()
#     else:
#         if rx_payload == 'busy':
#             console.print('[bright_red][ERROR][/] LoStik busy!')
#             exit(1)
#         if rx_payload == 'radio_err':
#             print('[ERROR] Time-out!')
#             exit(1)
#         if rx_payload == 'radio_rx  454F46': #EOF
#             print('End of file.')
#             break
#         rx_payload_list = rx_payload.split()
#         payload_hex = rx_payload_list[1]
#         received_hex_string_compressed = received_hex_string_compressed + payload_hex
#         print('Block received.')
#         lostik.rx(False)



# received_b64_bytes_compressed = bytes.fromhex(received_hex_string_compressed)
# del received_hex_string_compressed

# received_b64_bytes_decompressed = lzma.decompress(received_b64_bytes_compressed)
# del received_b64_bytes_compressed

# with open(file_name, 'wb') as file:
#     file.write(base64.b64decode(received_b64_bytes_decompressed))

# #check secure hash
# with open(file_name, 'rb') as file:
#     secure_hash = blake2b(digest_size=32)
#     secure_hash.update(file.read())

# if file_secure_hash != secure_hash.hexdigest():
#     print('[ERROR] Secure has mismatch.  File integrity check failed!')
#     os.remove(file_name)
#     exit(1)

# print('File integrity check PASSED!  File transfer complete.')

# exit(0)
