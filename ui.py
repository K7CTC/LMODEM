########################################################################
#                                                                      #
#          NAME:  LMODEM - UI Functions                                #
#  DEVELOPED BY:  Chris Clement (K7CTC)                                #
#       VERSION:  v0.7                                                 #
#                                                                      #
########################################################################

#standard library imports
from sys import exit
from time import sleep

#related third party imports
from rich.console import Console
from rich.theme import Theme

if __name__ == '__main__':
    print('[ERROR] ui.py is not intended for direct execution!')
    exit(1)

console = Console(theme=Theme(inherit=False))

if console.width < 80:
    print('[ERROR] Terminal width is less than 80 columns!')
    print('HELP: LMODEM minimal terminal size is 80x24. Resize and try again.')
    exit(1)

if console.height < 24:
    print('[ERROR] Terminal height is less than 24 rows!')
    print('HELP: LMODEM minimal terminal size is 80x24. Resize and try again.')
    exit(1)

def move_cursor(row, column):
    print(f'\033[{row};{column}H', end='')

def print_static_content():
    console.clear()
    console.print('[bright_white on deep_sky_blue4]LMODEM by Chris Clement (K7CTC)                                                 [/]')    # 1
    console.print('╭───────────────────────────────── Channel:   ─────────────────────────────────╮')                                       # 2
    console.print('                                                                                ')                                       # 3
    console.print('                             Frequency:                                         ')                                       # 4
    console.print('                                                                                ')                                       # 5
    console.print('╭─────────────────────────────────── Mode:   ──────────────────────────────────╮')                                       # 6
    console.print('                                                                                ')                                       # 7
    console.print('                             Bandwidth:                                         ')                                       # 8
    console.print('                              TX Power:                                         ')                                       # 9
    console.print('                      Spreading Factor:                                         ')                                       # 10
    console.print('                           Coding Rate:                                         ')                                       # 11
    console.print('                                                                                ')                                       # 12
    console.print('╭──────────────────────────────── File Details ────────────────────────────────╮')                                       # 13
    console.print('                                                                                ')                                       # 14
    console.print('                                  Name:                                         ')                                       # 15
    console.print('                        Size (on disk):                                         ')                                       # 16
    console.print('                   Size (over the air):                                         ')                                       # 17
    console.print('                                                                                ')                                       # 18
    console.print('╭─────────────────────────── File Transfer Progress ───────────────────────────╮')                                       # 19
    console.print('                                                                                ')                                       # 20
    console.print('[grey23]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   0% 0:00:00 0:00:00[/]')                            # 21
    console.print('                                                                                ')                                       # 22
    console.print('[grey15 on deep_sky_blue4]                                                           Press CTRL+C to quit.[/]')          # 23

def insert_module_version(module_version):
    move_cursor(1,77)
    console.print(f'[bright_white on deep_sky_blue4]{module_version}[/]')

def insert_lmodem_channel(lmodem_channel):
    move_cursor(2,45)
    console.print(lmodem_channel)

def insert_frequency(frequency):
    move_cursor(4,42)
    console.print(f'{frequency[:3]}.{frequency[3:]} MHz')

def insert_lmodem_mode(lmodem_mode):
    move_cursor(6,44)
    console.print(lmodem_mode)

def insert_bandwidth(bandwidth):
    move_cursor(8,42)
    console.print(f'{bandwidth} KHz')

def insert_power(power):
    move_cursor(9,42)
    label = 'NULL'
    dbm = '0.0dBm'
    mw = '0.0mW'
    ma = '0.0mA'
    if (int(power)) == 2:
        label = 'Low'
        dbm = '3.0dBm'
        mw = '2.0mW'
        ma = '42.6mA'
    if (int(power)) == 3:
        label = 'Low'
        dbm = '4.0dBm'
        mw = '2.5mW'
        ma = '44.8mA'
    if (int(power)) == 4:
        label = 'Low'
        dbm = '5.0dBm'
        mw = '3.2mW'
        ma = '47.3mA'
    if (int(power)) == 5:
        label = 'Low'
        dbm = '6.0dBm'
        mw = '4.0mW'
        ma = '49.6mA'
    if (int(power)) == 6:
        label = 'Low'
        dbm = '7.0dBm'
        mw = '5.0mW'
        ma = '52.0mA'
    if (int(power)) == 7:
        label = 'Medium'
        dbm = '8.0dBm'
        mw = '6.3mW'
        ma = '55.0mA'
    if (int(power)) == 8:
        label = 'Medium'
        dbm = '9.0dBm'
        mw = '7.9mW'
        ma = '57.7mA'
    if (int(power)) == 9:
        label = 'Medium'
        dbm = '10.0dBm'
        mw = '10.0mW'
        ma = '61.0mA'
    if (int(power)) == 10:
        label = 'Medium'
        dbm = '11.0dBm'
        mw = '12.6mW'
        ma = '64.8mA'
    if (int(power)) == 11:
        label = 'Medium'
        dbm = '12.0dBm'
        mw = '15.8mW'
        ma = '73.1mA'
    if (int(power)) == 12:
        label = 'Medium'
        dbm = '13.0dBm'
        mw = '20.0mW'
        ma = '78.0mA'
    if (int(power)) == 14:
        label = 'High'
        dbm = '14.7dBm'
        mw = '29.5mW'
        ma = '83.0mA'
    if (int(power)) == 15:
        label = 'High'
        dbm = '15.5dBm'
        mw = '35.5mW'
        ma = '88.0mA'
    if (int(power)) == 16:
        label = 'High'
        dbm = '16.3dBm'
        mw = '42.7mW'
        ma = '95.8mA'
    if (int(power)) == 17:
        label = 'High'
        dbm = '17.0dBm'
        mw = '50.1mW'
        ma = '103.6mA'
    if (int(power)) == 20:
        label = 'High'
        dbm = '18.5dBm'
        mw = '70.8mW'
        ma = '124.4mA'
    console.print(f'{label} ({dbm}/{mw}/{ma})')

def insert_spreading_factor(spreading_factor):
    move_cursor(10,42)
    console.print(spreading_factor)

def insert_coding_rate(coding_rate):
    move_cursor(11,42)
    console.print(coding_rate)

def insert_file_name(file_name):
    move_cursor(15,42)
    console.print(file_name)

def insert_file_size_on_disk(file_size):
    move_cursor(16,42)
    console.print(f'{file_size} bytes')

def insert_file_size_ota(file_size_ota):
    move_cursor(17,42)
    console.print(f'{file_size_ota} bytes')

def update_status(status):
    move_cursor(23,1)
    console.print('[bright_white on deep_sky_blue4]                                                           [/]')
    move_cursor(23,1)
    console.print(f'[bright_white on deep_sky_blue4]{status}[/]')
    move_cursor(23,80)

def splash_k7ctc():
    console.clear()
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

def splash_piers():
    console.clear()
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
    move_cursor(23,20)
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
