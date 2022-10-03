# LMODEM Notes

## LMODEM LoStik Modes

### MODE1 - Short Range (Fast)
* PWR = 6
* BW = 500
* SF = sf8
* CR = 4/6
* WDT = 875
* Block Size = 192 bytes
* Max OTA Size = 49152 bytes

It takes 166ms to send 192 bytes in MODE1

### MODE2 - Medium Range (Balanced)
* PWR = 12
* BW = 250
* SF = sf10
* CR = 4/7
* WDT = 1600
* Block Size = 128 bytes
* Max OTA Size = 32768

It takes 859ms to send 128 bytes in MODE2

### MODE3 - Long Range (Slow)
* PWR = 17
* BW = 125
* SF = sf12
* CR = 4/8
* WDT = 8500
* Block Size = 64 bytes
* Max OTA Size = 16384

It takes about 4336ms to send 64 bytes in MODE3

## LMODEM Channels
1. 914 MHz
2. 915 MHz
3. 916 MHz