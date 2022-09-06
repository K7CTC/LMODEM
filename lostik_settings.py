#Firmware Version
FIRMWARE_VERSION = 'RN2903 1.0.5 Nov 06 2018 10:45:27'

#Transmit Power (hardware default=20, script default=6)
#values: 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 20
SET_PWR = '6'
PWR_LABEL = 'LOW'

#Frequency (hardware default=923300000)
#value range: 902000000 to 928000000
SET_FREQ = '923300000'
FREQ_LABEL = '923.300 MHz'

#Spreading Factor (hardware default=sf12)
#values: sf7, sf8, sf9, sf10, sf11, sf12
SET_SF = 'sf7'
SF_LABEL = 7

#Radio Bandwidth (hardware default=125)
#values: 125, 250, 500
SET_BW = '250'
BW_LABEL = '250 KHz'

#Coding Rate (hardware default=4/5, script default=4/8)
#values: 4/5, 4/6, 4/7, 4/8
SET_CR = '4/5'
CR_LABEL = '4/5'

#Watchdog Timer Time-Out (hardware default=15000)
#value range: 0 to 4294967295 (0 disables wdt functionality)
SET_WDT = '15000'
WDT_LABEL = '15 seconds'

# #Modulation Mode (hardware default=lora)
# #this exists just in case the radio was somehow mistakenly set to FSK
# SET_MOD = 'lora'
# MOD_LABEL = 'LoRa'

# #CRC Header (hardware default=on)
# #values: on, off (not sure what this does, best to use default value)
# SET_CRC = 'on'
# CRC_LABEL = 'On'

# #IQ Inversion (hardware default=off)
# #values: on, off (not sure what this does, best to use default value)
# SET_IQI = 'off'
# IQI_LABEL = 'Off'

# #Sync Word (hardware default=34)
# #value: one hexadecimal byte
# SET_SYNC = '34'
# SYNC_LABEL = '34'
