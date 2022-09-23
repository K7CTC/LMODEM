########################################################################
#                                                                      #
#          NAME:  LMODEM - UI Functions                                #
#  DEVELOPED BY:  Chris Clement (K7CTC)                                #
#       VERSION:  v0.1                                                 #
#                                                                      #
########################################################################

#standard library imports
from sys import exit
from time import sleep

#local application/library specific imports
from console import console

if __name__ == '__main__':
    print('[ERROR] ui.py is not intended for direct execution!')
    exit(1)

def move_cursor(row, column):
    print(f'\033[{row};{column}H', end='')

def print_static_content():
    console.clear()
    console.print('[white on deep_sky_blue4] ⣿ LMODEM      by Chris Clement (K7CTC)  ❭❭❭                                    [/]')
    console.print('╭─ LoStik Parameters ──────────────────────────────────────────────────────────╮')
    console.print('           Firmware Version:')
    console.print('                    EUI-64™:')
    console.print('                  Frequency:')
    console.print('                  Bandwidth:')
    console.print('                   TX Power:')
    console.print('           Spreading Factor:')
    console.print('                Coding Rate:')
    console.print('╭─ LMODEM Parameters ──────────────────────────────────────────────────────────╮')
    console.print('                       Mode:')
    console.print('                    Channel:')
    console.print('╭─ File Transfer Details ──────────────────────────────────────────────────────╮')
    console.print('                       Name:')
    console.print('             Size (on disk):')
    console.print('        Size (over the air):')
    console.print('                Secure Hash:')
    console.print('                     Blocks:')
    console.print('╭─ File Transfer Progress ─────────────────────────────────────────────────────╮')
    console.print()
    console.print()
    console.print()
    console.print('[grey15 on deep_sky_blue4]                                                           Press CTRL+C to quit.[/]')



def insert_module_version(module_version):
    move_cursor(1,11)
    console.print(f'[white on deep_sky_blue4]{module_version}[/]')

def insert_module_name(module_name):
    move_cursor(1,47)
    console.print(f'[white on deep_sky_blue4]{module_name}[/]')
   
def insert_firmware_version(firmware_version):
    move_cursor(3,30)
    console.print(firmware_version)

def insert_hweui(hweui):
    move_cursor(4,30)
    console.print(hweui)

def insert_frequency(frequency):
    move_cursor(5,30)
    console.print(f'{frequency[:3]}.{frequency[3:]} MHz')

def insert_bandwidth(bandwidth):
    move_cursor(6,30)
    console.print(f'{bandwidth} KHz')

def insert_power(power):
    move_cursor(7,30)
    label = 'NULL'
    dbm = '0.0 dBm'
    mw = '0.0 mW'
    ma = '0.0 mA'
    if (int(power)) == 2:
        label = 'Low'
        dbm = '3.0 dBm'
        mw = '2.0 mW'
        ma = '42.6 mA'
    if (int(power)) == 3:
        label = 'Low'
        dbm = '4.0 dBm'
        mw = '2.5 mW'
        ma = '44.8 mA'
    if (int(power)) == 4:
        label = 'Low'
        dbm = '5.0 dBm'
        mw = '3.2 mW'
        ma = '47.3 mA'
    if (int(power)) == 5:
        label = 'Low'
        dbm = '6.0 dBm'
        mw = '4.0 mW'
        ma = '49.6 mA'
    if (int(power)) == 6:
        label = 'Low'
        dbm = '7.0 dBm'
        mw = '5.0 mW'
        ma = '52.0 mA'
    if (int(power)) == 7:
        label = 'Medium'
        dbm = '8.0 dBm'
        mw = '6.3 mW'
        ma = '55.0 mA'
    if (int(power)) == 8:
        label = 'Medium'
        dbm = '9.0 dBm'
        mw = '7.9 mW'
        ma = '57.7 mA'
    if (int(power)) == 9:
        label = 'Medium'
        dbm = '10.0 dBm'
        mw = '10.0 mW'
        ma = '61.0 mA'
    if (int(power)) == 10:
        label = 'Medium'
        dbm = '11.0 dBm'
        mw = '12.6 mW'
        ma = '64.8 mA'
    if (int(power)) == 11:
        label = 'Medium'
        dbm = '12.0 dBm'
        mw = '15.8 mW'
        ma = '73.1 mA'
    if (int(power)) == 12:
        label = 'Medium'
        dbm = '13.0 dBm'
        mw = '20.0 mW'
        ma = '78.0 mA'
    if (int(power)) == 14:
        label = 'High'
        dbm = '14.7 dBm'
        mw = '29.5 mW'
        ma = '83.0 mA'
    if (int(power)) == 15:
        label = 'High'
        dbm = '15.5 dBm'
        mw = '35.5 mW'
        ma = '88.0 mA'
    if (int(power)) == 16:
        label = 'High'
        dbm = '16.3 dBm'
        mw = '42.7 mW'
        ma = '95.8 mA'
    if (int(power)) == 17:
        label = 'High'
        dbm = '17.0 dBm'
        mw = '50.1 mW'
        ma = '103.6 mA'
    if (int(power)) == 20:
        label = 'High'
        dbm = '18.5 dBm'
        mw = '70.8 mW'
        ma = '124.4 mA'    
    console.print(f'{label} ({dbm} / {mw} / {ma})')

def insert_spreading_factor(spreading_factor):
    move_cursor(8,30)
    console.print(spreading_factor)

def insert_coding_rate(coding_rate):
    move_cursor(9,30)
    console.print(coding_rate)

def insert_lmodem_mode(lmodem_mode):
    move_cursor(11,30)
    console.print(lmodem_mode)

def insert_lmodem_channel(lmodem_channel):
    move_cursor(12,30)
    console.print(lmodem_channel)

def insert_file_name(file_name):
    move_cursor(14,30)
    console.print(file_name)

def insert_file_size(file_size):
    move_cursor(15,30)
    console.print(f'{file_size} bytes')

def insert_file_size_ota(file_size_ota):
    move_cursor(16,30)
    console.print(f'{file_size_ota} bytes')

def insert_secure_hash(secure_hash):
    move_cursor(17,30)
    console.print(secure_hash)

def insert_blocks(blocks):
    move_cursor(18,30)
    console.print(blocks)
    
def update_status(status):
    move_cursor(23,1)
    status = status.ljust(59)
    console.print(f'[white on deep_sky_blue4]{status}[/]')




def lostik_service_update_total_air_time(last_tx_air_time):
    move_cursor(12,30)
    global total_air_time
    total_air_time += last_tx_air_time
    total_air_time_seconds = total_air_time / 1000
    console.print(f'{total_air_time_seconds} seconds')
   
def splash():
    move_cursor(15,27)
    console.print('[grey70]C h r i s    C l e m e n t[/]') 
    
    callsign_elements = [
        '▰▰   ▰▰',
        '▰▰  ▰▰ ',
        '▰▰▰▰▰',
        '▰▰▰▰▰▰▰',
        '▰    ▰▰',
        '    ▰▰',
        '   ▰▰',
        ' ▰▰▰▰▰▰',
        '▰▰',
        '▰▰▰▰▰▰▰▰',
        '   ▰▰'
    ]
    
    frame_delay = .03

    #K
    move_cursor(9, 16)
    console.print(callsign_elements[0], style='color(26)')
    sleep(frame_delay)
    move_cursor(10, 16)
    console.print(callsign_elements[1], style='color(32)')
    sleep(frame_delay)
    move_cursor(11, 16)
    console.print(callsign_elements[2], style='color(38)')
    sleep(frame_delay)
    move_cursor(12, 16)
    console.print(callsign_elements[1], style='color(32)')
    sleep(frame_delay)
    move_cursor(13, 16)
    console.print(callsign_elements[0], style='color(26)')
    sleep(frame_delay)
    
    #7
    move_cursor(13, 26)
    console.print(callsign_elements[6], style='color(26)')
    sleep(frame_delay)
    move_cursor(12, 26)
    console.print(callsign_elements[6], style='color(32)')
    sleep(frame_delay)
    move_cursor(11, 26)
    console.print(callsign_elements[5], style='color(38)')
    sleep(frame_delay)
    move_cursor(10, 26)
    console.print(callsign_elements[4], style='color(32)')
    sleep(frame_delay)
    move_cursor(9, 26)
    console.print(callsign_elements[3], style='color(26)')
    sleep(frame_delay)
    
    #C
    move_cursor(9, 36)
    console.print(callsign_elements[7], style='color(26)')
    sleep(frame_delay)
    move_cursor(10, 36)
    console.print(callsign_elements[8], style='color(32)')
    sleep(frame_delay)
    move_cursor(11, 36)
    console.print(callsign_elements[8], style='color(38)')
    sleep(frame_delay)
    move_cursor(12, 36)
    console.print(callsign_elements[8], style='color(32)')
    sleep(frame_delay)
    move_cursor(13, 36)
    console.print(callsign_elements[7], style='color(26)')
    sleep(frame_delay)
    
    #T
    move_cursor(13, 46)
    console.print(callsign_elements[10], style='color(26)')
    sleep(frame_delay)
    move_cursor(12, 46)
    console.print(callsign_elements[10], style='color(32)')
    sleep(frame_delay)
    move_cursor(11, 46)
    console.print(callsign_elements[10], style='color(38)')
    sleep(frame_delay)
    move_cursor(10, 46)
    console.print(callsign_elements[10], style='color(32)')
    sleep(frame_delay)
    move_cursor(9, 46)
    console.print(callsign_elements[9], style='color(26)')
    sleep(frame_delay)
    
    #C
    move_cursor(9, 57)
    console.print(callsign_elements[7], style='color(26)')
    sleep(frame_delay)
    move_cursor(10, 57)
    console.print(callsign_elements[8], style='color(32)')
    sleep(frame_delay)
    move_cursor(11, 57)
    console.print(callsign_elements[8], style='color(38)')
    sleep(frame_delay)
    move_cursor(12, 57)
    console.print(callsign_elements[8], style='color(32)')
    sleep(frame_delay)
    move_cursor(13, 57)
    console.print(callsign_elements[7], style='color(26)')
    sleep(frame_delay)
    
    sleep(.5)

    move_cursor(19,30)
    console.print('[grey70]Proudly presents...[/]')

    sleep(1.5)
    console.clear()
    sleep(1)

    def logo_print_line(line, color):
        lines = [
            '╭─────────╮  ╭─╮  ╭─────────╮  ╭─────────╮  ╭─────────╮',
            '╰──────╮  │  ╰─╯  ╰─────────╯  ╰──────╮  │  │ ╭───────╯',
            '╭──────╯  │  ╭─╮  ╭───────╮    ╭──────╯  │  │ ╰───────╮',
            '│ ╭───────╯  │ │  │ ╭─────╯    │ ╭────╮  ⎨  ╰──────╮  │',
            '│ │          │ │  │ ╰───────╮  │ │    │  │  ╭──────╯  │',
            '╰─╯          ╰─╯  ╰─────────╯  ╰─╯    ╰──╯  ╰─────────╯'
        ]
        style = f'color({color})'
        if color == 0:
            lines[line] = '                                                       '
        row = line + 8
        column = 14
        move_cursor(row, column)
        console.print(lines[line], style=style)

    frame_delay = .06

    move_cursor(24,30)
    console.print('[grey30]Copyright © 2017-2022 Chris Clement (K7CTC)[/]')

    logo_print_line(0, 235)
    sleep(frame_delay)

    logo_print_line(1, 235)
    logo_print_line(0, 231)
    sleep(frame_delay)

    logo_print_line(2, 235)
    logo_print_line(1, 231)
    logo_print_line(0, 249)
    sleep(frame_delay)

    logo_print_line(3, 235)
    logo_print_line(2, 231)
    logo_print_line(1, 249)
    logo_print_line(0, 244)
    sleep(frame_delay)

    logo_print_line(4, 235)
    logo_print_line(3, 231)
    logo_print_line(2, 249)
    logo_print_line(1, 244)
    logo_print_line(0, 239)
    sleep(frame_delay)

    logo_print_line(5, 235)
    logo_print_line(4, 231)
    logo_print_line(3, 249)
    logo_print_line(2, 244)
    logo_print_line(1, 239)
    logo_print_line(0, 235)
    sleep(frame_delay)

    logo_print_line(5, 231)
    logo_print_line(4, 249)
    logo_print_line(3, 244)
    logo_print_line(2, 239)
    logo_print_line(1, 235)
    logo_print_line(0, 0)
    sleep(frame_delay)

    logo_print_line(5, 249)
    logo_print_line(4, 244)
    logo_print_line(3, 239)
    logo_print_line(2, 235)
    logo_print_line(1, 0)
    sleep(frame_delay)

    logo_print_line(5, 244)
    logo_print_line(4, 239)
    logo_print_line(3, 235)
    logo_print_line(2, 0)
    sleep(frame_delay)

    logo_print_line(5, 239)
    logo_print_line(4, 235)
    logo_print_line(3, 0)
    sleep(frame_delay)

    logo_print_line(5, 235)
    logo_print_line(4, 0)
    sleep(frame_delay)

    logo_print_line(5, 0)

    sleep(.25)

    frame_delay = .12

    logo_print_line(0, 235)
    logo_print_line(1, 235)
    logo_print_line(2, 235)
    logo_print_line(3, 235)
    logo_print_line(4, 235)
    logo_print_line(5, 235)
    sleep(frame_delay)

    logo_print_line(0, 231)
    logo_print_line(1, 231)
    logo_print_line(2, 231)
    logo_print_line(3, 231)
    logo_print_line(4, 231)
    logo_print_line(5, 231)
    sleep(frame_delay)

    logo_print_line(0, 253)
    logo_print_line(1, 253)
    logo_print_line(2, 253)
    logo_print_line(3, 253)
    logo_print_line(4, 253)
    logo_print_line(5, 253)
    sleep(frame_delay)

    logo_print_line(0, 249)
    logo_print_line(1, 249)
    logo_print_line(2, 249)
    logo_print_line(3, 249)
    logo_print_line(4, 249)
    logo_print_line(5, 249)

    sleep(.25)

    def title_print_line(color):
        style = f'color({color})'
        row = 15
        column = 22
        move_cursor(row, column)
        console.print('The Raspberry Pi Event Reporting System', style=style)

    title_print_line(235)
    sleep(frame_delay)

    title_print_line(231)
    sleep(frame_delay)

    title_print_line(253)
    sleep(frame_delay)

    title_print_line(249)

    sleep(3)