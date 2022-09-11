#Firmware Version
FIRMWARE_VERSION = 'RN2903 1.0.5 Nov 06 2018 10:45:27'

#Transmit Power (hardware default=2)
#values: 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 20
PWR = '6'

#LMODEM robustness options
# if args.power == 'low':
#     SET_PWR = b'6'
#     PWR_LABEL = 'LOW'
#     PWR_LABEL_DBM = '7.0 dBm'
#     PWR_LABEL_MW = '5.0 mW'
# elif args.power =='medium':
#     SET_PWR = b'12'
#     PWR_LABEL = 'MEDIUM'
#     PWR_LABEL_DBM = '13.0 dBm'
#     PWR_LABEL_MW = '20.0 mW'
# elif args.power == 'high':
#     SET_PWR = b'20'
#     PWR_LABEL = 'HIGH'
#     PWR_LABEL_DBM = '18.5 dBm'
#     PWR_LABEL_MW = '70.8 mW'

#Frequency (hardware default=923300000)
#value range: 902000000 to 928000000
FREQ = '923300000'

#Spreading Factor (hardware default=sf12)
#values: sf7, sf8, sf9, sf10, sf11, sf12
SF = 'sf8'

#Radio Bandwidth (KHz) (hardware default=125)
#values: 125, 250, 500
BW = '500'

#Coding Rate (FEC) (hardware default=4/5)
#values: 4/5, 4/6, 4/7, 4/8
CR = '4/6'

#Watchdog Timer Time-Out (milliseconds) (hardware default=15000)
#value range: 0 to 4294967295 (0 disables wdt functionality)
WDT = '15000'

#Modulation Mode (hardware default=lora)
#values: lora, fsk
MOD = 'lora'

#CRC Header (hardware default=on)
#values: on, off (not sure what this does, best to use default value)
CRC = 'on'

#IQ Inversion (hardware default=off)
#values: on, off (not sure what this does, best to use default value)
IQI = 'off'

#Sync Word (hardware default=34)
#value: one hexadecimal byte
SYNC = '34'
