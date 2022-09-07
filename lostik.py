########################################################################
#                                                                      #
#          NAME:  Ronoth LoStik Hardware Driver/Module                 #
#  DEVELOPED BY:  Chris Clement (K7CTC)                                #
#       VERSION:  v0.2.1                                               #
#                                                                      #
########################################################################

#import from required 3rd party libraries
from errno import ENOANO
import serial
import serial.tools.list_ports

#import from project library
import lostik_settings

#import from standard library
from sys import exit
from time import time

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

#function: read line from serial interface
# returns: ascii string
def read():
    line = lostik_port.readline().decode('ASCII').rstrip()
    return line

#function: write line to serial interface
# accepts: LoStik command as ascii string
def write(command):
    if type(command) != str:
        print('[ERROR] Failed to process LoStik command!')
        print('HELP: Invalid type, command must be a string.')
        exit(1)
    else:
        command = command.encode('ASCII')
        lostik_port.write(b''.join([command, b'\r\n']))

#function: read system firmware version from LoStik device
# returns: firmware version (as string)
def get_ver():
    write('sys get ver')
    return read()

#check LoStik firmware version before proceeding
if get_ver() != lostik_settings.FIRMWARE_VERSION:
    print('[ERROR] LoStik failed to return expected firmware version!')
    exit(1)

#function: disable LoRaWAN via "mac pause" command (page 25 in RN2903 command reference)
#    note: terminate on error
def disable_lorawan():
    write('mac pause')
    if read() != '4294967245':
        print('[ERROR] Failed to disable LoRaWAN!')
        exit(1)

#disable LoRaWAN before proceeding (required to issue commands directly to the radio)
disable_lorawan()

#functions: read radio settings from LoStik device
#  returns: setting value (as string)
def get_pwr():
    write('radio get pwr')
    return read()
def get_freq():
    write('radio get freq')
    return read()
def get_sf():
    write('radio get sf')
    return read()
def get_bw():
    write('radio get bw')
    return read()
def get_cr():
    write('radio get cr')
    return read()
def get_wdt():
    write('radio get wdt')
    return read()
def get_mod():
    write('radio get mod')
    return read()
def get_crc():
    write('radio get crc')
    return read()
def get_iqi():
    write('radio get iqi')
    return read()
def get_sync():
    write('radio get sync')
    return read()

#functions: write radio settings to LoStik device
#  accepts: setting value as ascii string
#     note: terminate on error
def set_pwr(pwr):
    write(f'radio set pwr {pwr}')
    if read() != 'ok':
        print('[ERROR] Failed to set LoStik transmit power!')
        exit(1)
def set_freq(freq):
    write(f'radio set freq {freq}')
    if read() != 'ok':
        print('[ERROR] Failed to set LoStik frequency!')
        exit(1)
def set_sf(sf):
    write(f'radio set sf {sf}')
    if read() != 'ok':
        print('[ERROR] Failed to set LoStik spreading factor!')
        exit(1)
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
def set_wdt(wdt):
    write(f'radio set wdt {wdt}')
    if read() != 'ok':
        print('[ERROR] Failed to set LoStik watchdog timer time-out!')
        exit(1)
def set_mod(mod):
    write(f'radio set mod {mod}')
    if read() != 'ok':
        print('[ERROR] Failed to set LoStik modulation mode!')
        exit(1)
def set_crc(crc):
    write(f'radio set crc {crc}')
    if read() != 'ok':
        print('[ERROR] Failed to set LoStik CRC header!')
        exit(1)
def set_iqi(iqi):
    write(f'radio set iqi {iqi}')
    if read() != 'ok':
        print('[ERROR] Failed to set LoStik IQ inversion!')
        exit(1)
def set_sync(sync):
    write(f'radio set sync {sync}')
    if read() != 'ok':
        print('[ERROR] Failed to set LoStik sync word!')
        exit(1)

#apply settings from lostik_settings.py
set_pwr(lostik_settings.PWR)
set_freq(lostik_settings.FREQ)
set_sf(lostik_settings.SF)
set_bw(lostik_settings.BW)
set_cr(lostik_settings.CR)

#function: obtain rssi of last received packet
# returns: rssi
def get_rssi():
    write('radio get rssi')
    rssi = read()
    return rssi

#function: obtain snr of last received packet
# returns: snr
def get_snr():
    write('radio get snr')
    snr = read()
    return snr

#function: control blue led
# accepts: boolean
def blue_led(state):
    if state == True:
        write('sys set pindig GPIO10 1') #GPIO10 1 = blue tx led on
    else:
        write('sys set pindig GPIO10 0') #GPIO10 0 = blue tx led off
    read()

#function: control red led
# accepts: boolean
def red_led(state):
    if state == True:
        write('sys set pindig GPIO11 1') #GPIO11 1 = red tx led on
    else:
        write('sys set pindig GPIO11 0') #GPIO11 0 = red tx led off
    read()

#function: attempt to transmit outbound packet
# accepts: packet as hex string
# returns: time_sent and air_time
#    note: terminate on error
def tx(packet):
    tx_start_time = 0
    tx_end_time = 0
    time_sent = 0
    air_time = 0
    write(f'radio tx {packet}')
    if read() == 'ok':
        tx_start_time = int(round(time()*1000))
        red_led(True)
    else:
        print('[ERROR] Transmit failure!')
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
# accepts: encoding (hex or ascii) - determines encoding of returned packet
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
    if reply == 'radio_err': #time-out
        return None
    reply = reply[10:] #remove 'radio_rx  ' from beginning of string
    if decode == False:
        return reply
    if decode == True:
        return bytes.fromhex(reply).decode('ASCII')

# #function: control lostik receive state
# # accepts: boolean
# #    note: terminate on error
# def rx(state):
#     if state == True:
#         #place LoStik in continuous receive mode
#         write('radio rx 0')
#         if read() == 'ok':
#             blue_led(True)
#         else:
#             print('[ERROR] Serial interface is busy, unable to communicate with LoStik!')
#             print('HELP: Disconnect and reconnect LoStik device, then try again.')
#             exit(1)
#     else:
#         #halt LoStik continuous receive mode
#         write('radio rxstop')
#         if read() == 'ok':
#             blue_led(False)
#         else:
#             print('[ERROR] Serial interface is busy, unable to communicate with LoStik!')
#             print('HELP: Disconnect and reconnect LoStik device, then try again.')
#             exit(1)
