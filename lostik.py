########################################################################
#                                                                      #
#          NAME:  Ronoth LoStik Hardware Driver/Module                 #
#  DEVELOPED BY:  Chris Clement (K7CTC)                                #
#       VERSION:  v0.2                                                 #
#                                                                      #
########################################################################

#import from required 3rd party libraries
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
# returns: ascii string from serial interface
def read():
    line = lostik_port.readline().decode('ASCII').rstrip()
    return line

#function: write command to serial interface
# accepts: command as ascii string
def write(command):
    if type(command) != str:
        print('[ERROR] Failed to process LoStik command!')
        print('HELP: Command must be of string type.')
        exit(1)
    else:
        command = command.encode('ASCII')
        lostik_port.write(b''.join([command, b'\r\n']))

#check LoStik firmware version before proceeding
write('sys get ver')
if read() != lostik_settings.FIRMWARE_VERSION:
    print('[ERROR] LoStik failed to return expected firmware version!')
    exit(1)

#attempt to pause mac (LoRaWAN) as required to issue commands directly to the radio
write('mac pause')
if read() != '4294967245':
    print('[ERROR] Failed to disable LoRaWAN!')
    exit(1)

#apply settings from lostik_settings.py
write(f'radio set pwr {lostik_settings.SET_PWR}')
if read() != 'ok':
    print('[ERROR] Failed to set LoStik transmit power!')
    exit(1)
write(f'radio set freq {lostik_settings.SET_FREQ}')
if read() != 'ok':
    print('[ERROR] Failed to set LoStik frequency!')
    exit(1)
write(f'radio set sf {lostik_settings.SET_SF}')
if read() != 'ok':
    print('[ERROR] Failed to set LoStik spreading factor!')
    exit(1)
write(f'radio set bw {lostik_settings.SET_BW}')
if read() != 'ok':
    print('[ERROR] Failed to set LoStik radio bandwidth!')
    exit(1)
write(f'radio set cr {lostik_settings.SET_CR}')
if read() != 'ok':
    print('[ERROR] Failed to set LoStik coding rate!')
    exit(1)
write(f'radio set wdt {lostik_settings.SET_WDT}')
if read() != 'ok':
    print('[ERROR] Failed to set LoStik watchdog timer time-out!')
    exit(1)

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

#function: control lostik receive state
# accepts: boolean
#    note: terminate on error
def rx(state):
    if state == True:
        #place LoStik in continuous receive mode
        write('radio rx 0')
        if read() == 'ok':
            blue_led(True)
        else:
            print('[ERROR] Serial interface is busy, unable to communicate with LoStik!')
            print('HELP: Disconnect and reconnect LoStik device, then try again.')
            exit(1)
    else:
        #halt LoStik continuous receive mode
        write('radio rxstop')
        if read() == 'ok':
            blue_led(False)
        else:
            print('[ERROR] Serial interface is busy, unable to communicate with LoStik!')
            print('HELP: Disconnect and reconnect LoStik device, then try again.')
            exit(1)

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
    response = ''
    while response == '':
        response = read()
    else:
        if response == 'radio_tx_ok':
            tx_end_time = int(round(time()*1000))
            time_sent = tx_end_time
            air_time = tx_end_time - tx_start_time
            red_led(False)
            return time_sent, air_time
        elif response == 'radio_err':
            print('[ERROR] Transmit failure!')
            exit(1)

def await_ack():
    rx(True)
    rx_payload = ''
    while rx_payload == '':
        rx_payload = read()
    else:
        if rx_payload == 'busy':
            print('[ERROR] LoStik busy!')
            exit(1)
        if rx_payload == 'radio_err':
            print('[ERROR] Reception failure or time-out occurred!')
            exit(1)
        if rx_payload == 'radio_rx 41434B':
            rx(False)
            return True

def send_ack():
    tx('41434B')