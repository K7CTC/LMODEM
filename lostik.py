########################################################################
#                                                                      #
#          NAME:  Ronoth LoStik Device Driver                          #
#  DEVELOPED BY:  Chris Clement (K7CTC)                                #
#       VERSION:  v0.8                                                 #
#                                                                      #
########################################################################

#import from required 3rd party libraries
from concurrent.futures.process import _chain_from_iterable_of_lists
import serial
import serial.tools.list_ports

#import from standard library
from sys import exit
from time import time, sleep

#terminate if executed directly
if __name__ == '__main__':
    print('[ERROR] lostik.py is not intended for direct execution!')
    exit(1)

#attempt LoStik detection, port assignment and connection
lostik_port_generator = serial.tools.list_ports.grep('1A86:7523')
lostik_count = 0
assigned_port = None
for detected_lostik in lostik_port_generator:
    lostik_count += 1
    assigned_port = detected_lostik.device
if lostik_count == 0:
    print('[ERROR] LoStik not detected!')
    print('HELP: Check serial port descriptor and/or device connection.')
    exit(1)
if lostik_count > 1:
    print('[ERROR] More than one LoStik detected!')
    print('HELP: Disconnect additional LoStik(s) and try again.')
    exit(1)
del lostik_port_generator, lostik_count
try:
    lostik_port = serial.Serial(assigned_port, baudrate=57600, timeout=1)
except:
    print('[ERROR] Unable to connect to LoStik!')
    print('HELP: Check port permissions. User must be member of "dialout" group on Linux.')
    exit(1)
del assigned_port

#function: read line from serial interface and remove CRLF from end
# returns: ascii string
def read():
    line = lostik_port.readline().decode('ASCII').rstrip()
    return line

#function: write line to serial interface
# accepts: LoStik command as ASCII string
def write(command):
    if type(command) != str:
        print('[ERROR] Failed to process LoStik command!')
        print('HELP: Invalid type, command must be a string.')
        exit(1)
    else:
        command = command.encode('ASCII')
        lostik_port.write(b''.join([command, b'\r\n']))

#function: get firmware version
# returns: firmware version
def get_ver():
    write('sys get ver')
    return read()

#confirm expected LoStik firmware version before proceeding
if get_ver() != 'RN2903 1.0.5 Nov 06 2018 10:45:27':
    print('[ERROR] LoStik failed to return expected firmware version!')
    exit(1)

#function: get LoStik EUI-64 (globally unique 64-bit identifier)
# returns: EUI-64
def get_hweui():
    write('sys get hweui')
    return read()

#function: control blue led
# accepts: boolean
def blue_led(state):
    if state == True:
        write('sys set pindig GPIO10 1') #GPIO10 1 = blue rx led on
    else:
        write('sys set pindig GPIO10 0') #GPIO10 0 = blue rx led off
    read()

#function: control red led
# accepts: boolean
def red_led(state):
    if state == True:
        write('sys set pindig GPIO11 1') #GPIO11 1 = red tx led on
    else:
        write('sys set pindig GPIO11 0') #GPIO11 0 = red tx led off
    read()

#function: disable LoRaWAN via "mac pause" command
#    note: terminate on error
def disable_lorawan():
    write('mac pause')
    if read() != '4294967245':
        print('[ERROR] Failed to disable LoRaWAN!')
        exit(1)

#disable LoRaWAN before proceeding (to issue commands directly to the radio)
disable_lorawan()

#functions: read radio settings from LoStik 
#  returns: setting value (as string)
def get_bw():
    write('radio get bw')
    return read()
def get_cr():
    write('radio get cr')
    return read()
def get_crc():
    write('radio get crc')
    return read()
def get_freq():
    write('radio get freq')
    return read()
def get_iqi():
    write('radio get iqi')
    return read()
def get_mod():
    write('radio get mod')
    return read()
def get_pwr():
    write('radio get pwr')
    return read()
def get_sf():
    write('radio get sf')
    return read()
def get_sync():
    write('radio get sync')
    return read()
def get_wdt():
    write('radio get wdt')
    return read()

#functions: write radio settings to LoStik 
#  accepts: setting value as ASCII string
#     note: terminate on error
def set_bw(bw):
    write(f'radio set bw {bw}')
    if read() != 'ok':
        print('[ERROR] Failed to set LoStik radio bandwidth!')
        exit(1)
def set_cr(cr):
    write(f'radio set cr {cr}')
    if read() != 'ok':
        print('[ERROR] Failed to set LoStik coding rate!')
        exit(1)
def set_crc(crc):
    write(f'radio set crc {crc}')
    if read() != 'ok':
        print('[ERROR] Failed to set LoStik CRC header!')
        exit(1)
def set_freq(freq):
    write(f'radio set freq {freq}')
    if read() != 'ok':
        print('[ERROR] Failed to set LoStik frequency!')
        exit(1)
def set_iqi(iqi):
    write(f'radio set iqi {iqi}')
    if read() != 'ok':
        print('[ERROR] Failed to set LoStik IQ inversion!')
        exit(1)
def set_mod(mod):
    write(f'radio set mod {mod}')
    if read() != 'ok':
        print('[ERROR] Failed to set LoStik modulation mode!')
        exit(1)
def set_pwr(pwr):
    write(f'radio set pwr {pwr}')
    if read() != 'ok':
        print('[ERROR] Failed to set LoStik transmit power!')
        exit(1)
def set_sf(sf):
    write(f'radio set sf {sf}')
    if read() != 'ok':
        print('[ERROR] Failed to set LoStik spreading factor!')
        exit(1)
def set_sync(sync):
    write(f'radio set sync {sync}')
    if read() != 'ok':
        print('[ERROR] Failed to set LoStik sync word!')
        exit(1)
def set_wdt(wdt):
    write(f'radio set wdt {wdt}')
    if read() != 'ok':
        print('[ERROR] Failed to set LoStik watchdog timer time-out!')
        exit(1)

#function: obtain received signal strength indicator of last received packet
# returns: rssi
def get_rssi():
    write('radio get rssi')
    rssi = read()
    return rssi

#function: obtain signal-to-noise ratio of last received packet
# returns: snr
def get_snr():
    write('radio get snr')
    snr = read()
    return snr

#function: attempt to transmit outbound packet
# accepts: packet as hexadecimal string by default, optionally accepts ASCII string
#  option: encode (boolean) - allows function to accept and encode ASCII instead of hexadecimal
# returns: time_sent and air_time
#    note: terminate on error
def tx(packet, encode = False):
    wdt = get_wdt()
    #sleep to prevent packet loss
    if wdt == '750':
        sleep(.1)
    if wdt == '1500':
        sleep(.15)
    if wdt == '8500':
        sleep(.2)
    tx_start_time = 0
    tx_end_time = 0
    time_sent = 0
    air_time = 0
    if encode == False:
        write(f'radio tx {packet}')
    if encode == True:
        hex = packet.encode('ASCII').hex()
        write(f'radio tx {hex}')
    if read() == 'ok':
        tx_start_time = int(round(time()*1000))
        red_led(True)
    else:
        print('[ERROR] Transmit failure!')
        print('HELP: Did you set the encode argument correctly?')
        exit(1)
    reply = ''
    while reply == '':
        reply = read()
    if reply == 'radio_tx_ok':
        tx_end_time = int(round(time()*1000))
        time_sent = tx_end_time
        air_time = tx_end_time - tx_start_time
        red_led(False)
        return time_sent, air_time
    elif reply == 'radio_err':
        print('[ERROR] Transmit failure!')
        exit(1)

#function: attempt to receive inbound packet
#  option: decode (boolean) - allows returned packed to be decoded from hexadecmial to ASCII
# returns: packet contents in chosen encoding or none if no packet received before time-out
def rx(decode = False):
    write('radio rx 0')
    if read() != 'ok':
        print('[ERROR] Serial interface is busy, unable to communicate with LoStik!')
        print('HELP: Disconnect and reconnect LoStik device, then try again.')
        exit(1)
    blue_led(True)
    reply = ''
    while reply == '':
        reply = read()
    blue_led(False)
    if reply == 'busy':
        print('[ERROR] LoStik busy!')
        exit(1)
    if reply == 'radio_err': #wdt time-out
        return 'TIME-OUT'
    reply = reply[10:] #remove 'radio_rx  ' from beginning of string
    if decode == False:
        return reply
    if decode == True:
        return bytes.fromhex(reply).decode('ASCII')

#function: force radio to halt continuous receive mode
#    note: terminate on error
def rxstop():
    write('radio rxstop')
    if read() == 'ok':
        blue_led(False)
    else:
        print('[ERROR] Serial interface is busy, unable to communicate with LoStik!')
        print('HELP: Disconnect and reconnect LoStik device, then try again.')
        exit(1)

########################################################################
# Below are LMODEM specific functions                                  #
########################################################################

#function: set LMODEM communication mode
# accepts: mode number (1, 2 or 3)
def lmodem_set_mode(mode_number): #pwr set to 2 for testing
    if mode_number > 3 or mode_number < 1:
        print('[ERROR] Invalid LMODEM mode!')
        print('HELP: Valid mode numbers are 1, 2, and 3.')
        exit(1)
    if mode_number == 1:
        set_pwr('2')
        # set_pwr('6')
        set_bw('500')
        set_sf('sf8')
        set_cr('4/6')
        set_wdt('750')
    if mode_number == 2:
        set_pwr('2')
        # set_pwr('12')
        set_bw('250')
        set_sf('sf10')
        set_cr('4/7')
        set_wdt('1500')
    if mode_number == 3:
        set_pwr('2')
        # set_pwr('17')
        set_bw('125')
        set_sf('sf12')
        set_cr('4/8')
        set_wdt('8500')

def lmodem_get_mode(): #pwr set to 2 for testing
    pwr = get_pwr()
    bw = get_bw()
    sf = get_sf()
    cr = get_cr()
    wdt = get_wdt()
    if pwr == '2' and bw == '500' and sf == 'sf8' and cr == '4/6' and wdt == '750':
    # if pwr == '6' and bw == '500' and sf == 'sf8' and cr == '4/6' and wdt == '750':
        return 1
    if pwr == '2' and bw == '250' and sf == 'sf10' and cr == '4/7' and wdt == '1500':
    # if pwr == '12' and bw == '250' and sf == 'sf10' and cr == '4/7' and wdt == '1500':
        return 2
    if pwr == '2' and bw == '125' and sf == 'sf12' and cr == '4/8' and wdt == '8500':
    # if pwr == '17' and bw == '125' and sf == 'sf12' and cr == '4/8' and wdt == '8500':
        return 3
    print('[ERROR] Invalid LoStik configuration!')
    print('HELP: LoStik settings do not match any of the LMODEM modes.')
    exit(1)
    
def lmodem_set_channel(channel_number):
    if channel_number >3 or channel_number < 1:
        print('[ERROR] Invalid channel number!')
        print('HELP: Valid channel numbes are 1, 2 and 3.')
    if channel_number == 1:
        set_freq('914000000')
    if channel_number == 2:
        set_freq('915000000')
    if channel_number == 3:
        set_freq('916000000')

def lmodem_get_channel():
    freq = get_freq()
    if freq == '914000000':
        return 1
    if freq == '915000000':
        return 2
    if freq == '916000000':
        return 3
    