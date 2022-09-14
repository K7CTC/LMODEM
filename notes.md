# LMODEM Notes

## Control Codes
* DTR = Data Terminal Ready
* TOT = Time-Out Timer
* DUP = Duplicate File
* CAN = Cancel File Transfer 
* RTR = Ready to Receive
* REQ = Request Blocks (list)
* SNT = Requested Blocks Sent
* FIN = File Transfer Finished

## LMODEM LoStik Modes

### MODE1 - Fastest & Least Robust
* PWR = 6
* BW = 500
* SF = sf8
* CR = 4/6
* WDT = 750
It takes about 125ms to send 128 bytes in MODE1

### MODE2 - Middle Ground
* PWR = 12
* BW = 250
* SF = sf10
* CR = 4/7
* WDT = 1500
It takes about 850ms to send 128 bytes in MODE2

### MODE3 - Slowest & Most Robust
* PWR = 17
* BW = 125
* SF = sf12
* CR = 4/8
* WDT = 8125
It takes about 7750ms to send 128 bytes in MODE3

## LMODEM Channels
1. 914 MHz
2. 915 MHz
3. 916 MHz