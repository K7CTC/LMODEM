########################################################################
#                                                                      #
#          NAME:  LMODEM - Console Parameters                          #
#  DEVELOPED BY:  Chris Clement (K7CTC)                                #
#       VERSION:  v0.8                                                 #
#                                                                      #
########################################################################

#standard library imports
from sys import exit

#related third party imports
from rich.console import Console
from rich.theme import Theme

if __name__ == '__main__':
    print('[ERROR] console.py is not intended for direct execution!')
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
