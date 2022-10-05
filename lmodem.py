########################################################################
#                                                                      #
#          NAME:  LMODEM                                               #
#  DEVELOPED BY:  Chris Clement (K7CTC)                                #
#       VERSION:  v0.6-dev                                             #
#                                                                      #
########################################################################

#standard library imports
import lzma
import os
import textwrap
import argparse
import json
from sys import exit
from hashlib import blake2b
from base64 import b85encode, b85decode
from pathlib import Path

#related third party imports
import rich.progress

#local application/library specific imports
import lostik
import ui

#establish and parse command line arguments
parser = argparse.ArgumentParser(description='LMODEM v0.6',
                                 epilog='Created by Chris Clement (K7CTC).')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-s', '--send',
                   help='send the specified file',
                   metavar='filename')
group.add_argument('-r', '--receive',
                   help='receive an incoming file',
                   action='store_true')
parser.add_argument('-c', '--channel',
                    help='LMODEM channel (default: 2)',
                    type=int,
                    choices=[1,2,3],
                    default=2)
parser.add_argument('-m', '--mode',
                    help='LMODEM mode (default: 1)',
                    type=int,
                    choices=[1,2,3],
                    default=1)
args = parser.parse_args()
del group, parser

#function: set LMODEM communication channel (frequency)
# accepts: channel number (1, 2 or 3)
def lmodem_set_channel(channel_number):
    if channel_number == 1:
        lostik.set_freq('914000000')
    if channel_number == 2:
        lostik.set_freq('915000000')
    if channel_number == 3:
        lostik.set_freq('916000000')

#function: get LMODEM communication channel (frequency)
# returns: channel number (1, 2 or 3)
def lmodem_get_channel():
    freq = lostik.get_freq()
    if freq == '914000000':
        return 1
    if freq == '915000000':
        return 2
    if freq == '916000000':
        return 3
    ui.update_status('[red1 on deep_sky_blue4][ERROR][/] Failed to get LMODEM channel!')
    exit(1)

#function: set LMODEM communication mode
# accepts: mode number (1, 2 or 3)
def lmodem_set_mode(mode_number): #pwr set to 2 for testing
    if mode_number == 1:
        lostik.set_pwr('2')
        # lostik.set_pwr('6')
        lostik.set_bw('500')
        lostik.set_sf('sf8')
        lostik.set_cr('4/6')
        lostik.set_wdt('1000')
    if mode_number == 2:
        lostik.set_pwr('2')
        # lostik.set_pwr('12')
        lostik.set_bw('250')
        lostik.set_sf('sf10')
        lostik.set_cr('4/7')
        lostik.set_wdt('2000')
    if mode_number == 3:
        lostik.set_pwr('2')
        # lostik.set_pwr('17')
        lostik.set_bw('125')
        lostik.set_sf('sf12')
        lostik.set_cr('4/8')
        lostik.set_wdt('5000')

#function: get LMODEM communication mode
# returns: mode number (1, 2 or 3)
def lmodem_get_mode(): #pwr set to 2 for testing
    pwr = lostik.get_pwr()
    bw = lostik.get_bw()
    sf = lostik.get_sf()
    cr = lostik.get_cr()
    wdt = lostik.get_wdt()
    if pwr == '2' and bw == '500' and sf == 'sf8' and cr == '4/6' and wdt == '1000':
    # if pwr == '6' and bw == '500' and sf == 'sf8' and cr == '4/6' and wdt == '1000':
        return 1
    if pwr == '2' and bw == '250' and sf == 'sf10' and cr == '4/7' and wdt == '2000':
    # if pwr == '12' and bw == '250' and sf == 'sf10' and cr == '4/7' and wdt == '2000':
        return 2
    if pwr == '2' and bw == '125' and sf == 'sf12' and cr == '4/8' and wdt == '5000':
    # if pwr == '17' and bw == '125' and sf == 'sf12' and cr == '4/8' and wdt == '5000':
        return 3
    ui.update_status('[red1 on deep_sky_blue4][ERROR][/] Failed to get LMODEM mode!')
    exit(1)

#initialize user interface
ui.console.show_cursor(False)
#ui.splash()
ui.print_static_content()
ui.insert_module_version('v0.6')

#initialize LoStik
lmodem_set_channel(args.channel)
lmodem_set_mode(args.mode)

#display LMODEM channel details
ui.insert_lmodem_channel(lmodem_get_channel())
ui.insert_frequency(lostik.get_freq())

#display LMODEM mode details
ui.insert_lmodem_mode(lmodem_get_mode())
ui.insert_bandwidth(lostik.get_bw())
ui.insert_power(lostik.get_pwr())
ui.insert_spreading_factor(lostik.get_sf())
ui.insert_coding_rate(lostik.get_cr())

#allow CTRL+C to gracefully terminate LMODEM
try:
    #sending file
    if args.send:
        outgoing_file = args.send

        #display outgoing file name
        ui.insert_file_name(outgoing_file)

        #check if outgoing file actually exists
        if not Path(outgoing_file).is_file():
            ui.update_status('[red1 on deep_sky_blue4][ERROR][/] File does not exist!')
            exit(1)

        #check if outgoing file name exceeds LMODEM maximum length of 32 characters
        if len(outgoing_file) > 32:
            ui.update_status('[red1 on deep_sky_blue4][ERROR][/] File name exceeds 32 character limit!')
            exit(1)

        #generate secure hash hex digest for outgoing file
        with open(outgoing_file, 'rb') as file:
            outgoing_file_secure_hash = blake2b(digest_size=16)
            outgoing_file_secure_hash.update(file.read())
            outgoing_file_secure_hash_hex_digest = outgoing_file_secure_hash.hexdigest()
            del outgoing_file_secure_hash

        #compress outgoing file (in memory) using lzma algorithm
        with open(outgoing_file, 'rb') as file:
            outgoing_file_compressed = lzma.compress(file.read())

        #base85 encode compressed outgoing file
        outgoing_file_compressed_b85 = b85encode(outgoing_file_compressed)
        del outgoing_file_compressed

        #determine outgoing file size over the air in bytes
        outgoing_file_size_ota = len(outgoing_file_compressed_b85)

        #display outgoing file size over the air
        ui.insert_file_size_ota(outgoing_file_size_ota)

        #check if outgoing file size over-the-air exceeds LMODEM maximum for chosen mode
        maximum_ota_file_size = 0
        if args.mode == 1:
            maximum_ota_file_size = 49152
        if args.mode == 2:
            maximum_ota_file_size = 32768
        if args.mode == 3:
            maximum_ota_file_size = 16384
        if outgoing_file_size_ota > maximum_ota_file_size:
            ui.update_status(f'[red1 on deep_sky_blue4][ERROR][/] Size (over the air) exceeds maximum of {maximum_ota_file_size} bytes for mode {args.mode}!')
            exit(1)
        del maximum_ota_file_size

        #determine outgoing file size on disk in bytes
        outgoing_file_size_on_disk = Path(outgoing_file).stat().st_size

        #display outgoing file size on disk
        ui.insert_file_size_on_disk(outgoing_file_size_on_disk)

        #hex encode base85 encoded compressed outgoing file
        outgoing_file_compressed_b85_hex = outgoing_file_compressed_b85.hex()
        del outgoing_file_compressed_b85

        #split hex encoded base85 encoded compressed outgoing file into blocks sized for chosen mode
        block_size = 0
        if args.mode == 1:
            block_size = 128 * 2
        if args.mode == 2:
            block_size = 128 * 2
        if args.mode == 3:
            block_size = 64 * 2
        blocks = textwrap.wrap(outgoing_file_compressed_b85_hex, block_size)
        del block_size, outgoing_file_compressed_b85_hex

        #obtain block count
        block_count = len(blocks)

        #concatenate zero filled block index and block contents to create numbered packets
        packets = []
        for block in blocks:
            block_index_zfill = str(blocks.index(block)).zfill(3)
            block_index_zfill_hex = block_index_zfill.encode('ASCII').hex()
            del block_index_zfill
            packet = block_index_zfill_hex + block
            packets.append(packet)
        del blocks

        #sub function: send requested blocks
        #     accepts: received block count, requested blocks list
        def send_requested_blocks(received_block_count, requested_blocks):
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
                    lostik.tx(packets[int(block_number)])
                    sent_block_count += 1
                    progress.update(task, completed=received_block_count+sent_block_count)
            lostik.tx('END_OF_TRANSMISSION', encode=True)
            ui.update_status('All requested blocks have been sent.')

        #basic handshake
        ui.update_status('Connecting...')
        while True:
            if lostik.rx(decode=True) == 'READY':
                lostik.tx('READY', encode=True)
                break
        ui.update_status('Connected!')

        #provide receiving station with the file transfer details
        #file name | size on disk | size over the air | number of blocks | secure hash
        file_transfer_details = (outgoing_file + '|' +
                                str(outgoing_file_size_on_disk) + '|' +
                                str(outgoing_file_size_ota) + '|' +
                                str(block_count) + '|' +
                                outgoing_file_secure_hash_hex_digest)
        del outgoing_file_size_on_disk, outgoing_file_size_ota, outgoing_file_secure_hash_hex_digest
        ui.update_status('Transmitting file transfer details.')
        lostik.tx(file_transfer_details, encode=True)
        del file_transfer_details
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
                send_requested_blocks(received_block_count, requested_blocks)
                del requested_blocks
            else:
                ui.update_status('Resuming file transfer.')
                requested_block_numbers = reply[3:]
                requested_blocks = requested_block_numbers.split('|')
                del requested_block_numbers
                send_requested_blocks(received_block_count, requested_blocks)
                del requested_blocks
            del received_block_count
        del reply

        #await reply after sending requested packets
        ui.update_status('Awaiting transfer result from receive station.')
        lostik.set_wdt(15000)
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

    #receiving file
    if args.receive:
        #basic handshake
        ui.update_status('Connecting...')
        while True:
            lostik.tx('READY', encode=True)
            if lostik.rx(decode=True) == 'READY':
                break
        ui.update_status('Connected!')

        #listen for incoming file details
        ui.update_status('Awaiting file transfer details.')
        file_transfer_details_string = lostik.rx(decode=True)
        if file_transfer_details_string == 'TIME-OUT':
            ui.update_status('[red1 on deep_sky_blue4][ERROR][/] LoStik watchdog timer time-out!')
            exit(1)
        else:
            file_transfer_details = file_transfer_details_string.split('|')
            incoming_file_name = file_transfer_details[0]
            incoming_file_size_on_disk = file_transfer_details[1]
            incoming_file_size_ota = file_transfer_details[2]
            incoming_file_block_count = file_transfer_details[3]
            incoming_file_secure_hash_hex_digest = file_transfer_details[4]
            del file_transfer_details
        del file_transfer_details_string

        #display file transfer details
        ui.update_status('Received file transfer details.')
        ui.insert_file_name(incoming_file_name)
        ui.insert_file_size_on_disk(incoming_file_size_on_disk)
        ui.insert_file_size_ota(incoming_file_size_ota)
        del incoming_file_size_on_disk, incoming_file_size_ota

        #if present, process existing file
        if Path(incoming_file_name).is_file():
            with open(incoming_file_name, 'rb') as file:
                local_file_secure_hash = blake2b(digest_size=16)
                local_file_secure_hash.update(file.read())
            if incoming_file_secure_hash_hex_digest == local_file_secure_hash.hexdigest():
                ui.update_status('[green1 on deep_sky_blue4][DONE][/] Duplicate file found. Integrity check passed.')
                lostik.tx('DUPLICATE_PASS', encode=True)
                exit(0)
            if incoming_file_secure_hash_hex_digest != local_file_secure_hash.hexdigest():
                ui.update_status('[red1 on deep_sky_blue4][ERROR][/] Duplicate filename found. Integrity check failed!')
                lostik.tx('DUPLICATE_FAIL', encode=True)
                exit(1)

        #initialize dictionary to temporarily store received blocks
        received_blocks = {}

        #function: obtain the number of received blocks
        # returns: received block count (int)
        def count_received_blocks():
            received_block_count = 0
            for block in received_blocks:
                if received_blocks[block] != '':
                    received_block_count += 1
            return received_block_count

        #function: deposit received blocks into dictionary
        def receive_requested_blocks():
            ui.update_status('Receiving requested blocks.')
            ui.move_cursor(21,1)
            progress = rich.progress.Progress(rich.progress.BarColumn(bar_width=59),
                                            rich.progress.TaskProgressColumn(),
                                            rich.progress.TimeRemainingColumn(),
                                            rich.progress.TimeElapsedColumn())
            task = progress.add_task('Receive Requested Blocks', total=int(incoming_file_block_count))
            with progress:
                progress.update(task, completed=count_received_blocks())
                timeout_counter = 0
                while True:
                    incoming_packet = lostik.rx()
                    if incoming_packet == '454E445F4F465F5452414E534D495353494F4E': #END_OF_TRANSMISSION
                        break
                    if incoming_packet == 'TIME-OUT':
                        timeout_counter += 1
                        if timeout_counter == 3:
                            break
                        continue
                    incoming_block_number_hex = incoming_packet[:6]
                    incoming_block_number = bytes.fromhex(incoming_block_number_hex).decode('ASCII')
                    incoming_block = incoming_packet[6:]
                    received_blocks.update({incoming_block_number: incoming_block})
                    progress.update(task, completed=count_received_blocks())

        #function: build string of pipe delimited missing block numbers, if any
        # returns: missing blocks string
        def create_missing_block_numbers_string(received_blocks):
            missing_block_numbers_string = ''
            for block in received_blocks:
                if received_blocks[block] == '':
                    missing_block_numbers_string = missing_block_numbers_string + str(block) + '|'
            if len(missing_block_numbers_string) != 0:
                missing_block_numbers_string = missing_block_numbers_string[:-1]
            return missing_block_numbers_string

        #check for partial file and transfer from disk to memory if found
        partial_file_name = incoming_file_name + '.json'
        if Path(partial_file_name).is_file():
            with open(partial_file_name) as json_file:
                received_blocks.clear()
                received_blocks = json.load(json_file)
            os.remove(partial_file_name)
        del partial_file_name

        #determine whether to resume a partial transfer or start fresh
        resume = False
        if 'secure_hash_hex_digest' in received_blocks:
            if incoming_file_secure_hash_hex_digest == received_blocks['secure_hash_hex_digest']:
                received_blocks.pop('secure_hash_hex_digest')
                resume = True
        if resume == True:
            missing_block_numbers = create_missing_block_numbers_string(received_blocks)
            #cap requested blocks at 32 (to limit packet size)
            if len(missing_block_numbers) > 127:
                missing_block_numbers = missing_block_numbers[:127]
            received_block_count = str(count_received_blocks()).zfill(3)
            block_request_details = received_block_count + missing_block_numbers
            del received_block_count, missing_block_numbers
            ui.update_status('Resuming file transfer.')
            lostik.tx(block_request_details, encode=True)
            del block_request_details
            receive_requested_blocks()
        elif resume == False:
            #initialize key:value pairs based on incoming file block count
            received_blocks.clear()
            keys = []
            for i in range(int(incoming_file_block_count)):
                keys.append(str(i).zfill(3))
            received_blocks = dict.fromkeys(keys, '')
            received_block_count = '000'
            block_request_details = received_block_count
            del received_block_count
            ui.update_status('Starting file transfer.')
            lostik.tx(block_request_details, encode=True)
            del block_request_details
            receive_requested_blocks()
        del resume

        #process received blocks
        if count_received_blocks() == int(incoming_file_block_count):
            del incoming_file_block_count
            ui.update_status('All blocks received. Processing file...')
            #concatenate blocks
            incoming_file_compressed_b85_hex = ''
            for block in received_blocks.values():
                incoming_file_compressed_b85_hex = incoming_file_compressed_b85_hex + block
            del received_blocks
            #decode from hex
            incoming_file_compressed_b85 = bytes.fromhex(incoming_file_compressed_b85_hex)
            del incoming_file_compressed_b85_hex
            #decode from b85
            incoming_file_compressed = b85decode(incoming_file_compressed_b85)
            del incoming_file_compressed_b85
            #decompress
            incoming_file = lzma.decompress(incoming_file_compressed)
            del incoming_file_compressed
            #write to disk
            with open(incoming_file_name, 'wb') as file:
                file.write(incoming_file)
            del incoming_file
            #obtain secure hash
            with open(incoming_file_name, 'rb') as file:
                incoming_file_secure_hash = blake2b(digest_size=16)
                incoming_file_secure_hash.update(file.read())
            if incoming_file_secure_hash_hex_digest != incoming_file_secure_hash.hexdigest():
                ui.update_status('[red1 on deep_sky_blue4][ERROR][/] File transfer complete. Integrity check failed!')
                os.remove(incoming_file_name)
                del incoming_file_name
                lostik.tx('COMPLETE_FAIL', encode=True)
                exit(1)
            if incoming_file_secure_hash_hex_digest == incoming_file_secure_hash.hexdigest():
                ui.update_status('[green1 on deep_sky_blue4][DONE][/] File transfer complete. Integrity check passed.')
                lostik.tx('COMPLETE_PASS', encode=True)
                exit(0)
        else:
            ui.update_status('[orange1 on deep_sky_blue4][WARNING][/] File transfer incomplete. Try again to resume.')
            received_blocks['secure_hash_hex_digest'] = incoming_file_secure_hash_hex_digest
            del incoming_file_secure_hash_hex_digest
            partial_file_name = incoming_file_name + '.json'
            del incoming_file_name
            with open(partial_file_name, 'w') as json_file:
                json.dump(received_blocks, json_file, indent=4)
            lostik.tx('INCOMPLETE', encode=True)
            exit(1)

except KeyboardInterrupt:
    ui.console.show_cursor(True)
    exit(2)
