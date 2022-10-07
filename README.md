# LMODEM

LMODEM is the world's first file transfer protocol purpose built for LoRa.  The name is a throwback to X, Y, and ZMODEM that I used heavily back when I was a BBS SysOp.

## Why?

The short answer, just to see if it was possible.  After completing work on my LoRa chat application I had all the requisite knowledge for sending and receiving ASCII bytes over LoRa.  One day I thought to myself how neat it would be to transfer an arbitrary file over LoRa.  I searched the internet for days looking for any examples of anyone attempting this feat.  Apparenly I was the first person, so I took it as a personal challenge to scratch build a protocol for the sole purpose of proving that I could transfer files over LoRa.

## Limitations

* Maximum file name length of 32 characters.
* Maximim range ~20 miles line of sight.

## Features

* File integrity check using BLAKE2b secure hash algorithm provides 100% confidence in transferred files.
* Lempel-Ziv Markov chain Algorithm (LZMA) compression significantly reduces "over the air" file size.
* Partial transfer resume.  You can reattempt as many times as is necessary to finish an incomplete transfer without having to start over.
* LMODEM "modes" simplify underlying LoRa settings and provide a user friendly experience.
* LMODEM "channels" eliminate the need for users to manually specify an operating frequency.

## Operating Principles

The sending station takes a file (in the current working directory) as input.  The protocol performs some quick checks on the file first.  It checks that the file exists.  It gets the file size (on disk).  It checks that the filename does not exceed 32 characters.  It generates a secure has for the file with a message digest size of 32 bytes.  The file is then compressed (in memory) using LZMA.  The compressed file undergoes binary to text encoding using the Base85 encoding scheme.  Base85 is more efficient than Base64 and maintains compatibility with LoRa.  LMODEM then checks that the compressed and encoded file does not exceed 32kb.  32kb is the maximum over-the-air file size.  The file is then encoded in hexadecimal.  The file is then divided into 128 byte blocks (with any remainder in the final block).  The block numbers (zero padded) are then prefixed to the blocks themselves, thus creating the packets that will be sent over the air.  The sending station is now ready to present the file to the receiving station.

Once a basic handshake is performed, both the sending and receiving stations are "synchronized" and the sending station sends the file transfer details packet.  This packet consists of:

* Filename
* Size on disk (in bytes)
* Size over the air (in bytes)
* Block count
* Secure hash

The receiving station processes the file transfer details packet as follows:

* It displays the file transfer details to the user.
* It checks to see if the incoming file already exists.
    - If so, it compares the secure hash to see if the file is a duplicate.
        + If so, it tells the sending station that the file is a dupe and the transfer is aborted.
        + If not, the user and the sending station is informed that a file with the same name exists.
* It checks if a partial file exists.  If so, it is transferred from disk to memory.
* It checks the secure hash (stored in the partial file) against the incoming file.
    - If the hash matches, the file transfer is resumed.
        + Missing blocks are enumerated and requested from the sending station.
    - If the hash does not match, the partial file is purged from memory and the transfer begins.

The sending station is therefore requested to send all or a subset of file blocks.  When this task is completed, the sending station notifies the receiving station that all requested blocks have been sent.

The receiving station checks for any missing blocks.  If there are missing blocks, the secure hash of the incoming file is appended and a partial file is written to disk.  The users on both ends are instructed to try again.  It is suggested that a more robust LMODEM mode is selected.

If there are no missing blocks.  The receiving station reconstitues the file:

* The hexadecimal encoded blocks are sequentially concatenated into a single blob.
* The blob is decoded from hexadecimal back into Base85 encoded ASCII bytes.
* The blob is converted from Base85 back into binary.
* The binary blob is then decompressed (using LZMA).
* The decompressed binary is then written to disk (using the file name provided in the file transfer details).
* The file on disk is then hashed using BLAKE2b.
* The secure hashes are compared to guarantee file integrity.
* If the integrity check fails, the file is removed from disk.




## LMODEM Modes

### MODE 1 - Minimum Range for Bench Testing (21875 bps hardware maximum)
* PWR = 2
* BW = 500
* SF = sf7
* CR = 4/5
* WDT = 1000                            
* Block Size = 128 bytes
* Max OTA Size = 32768 bytes
* Max Requested Block Count = 32
* Data Rate = 21875 bps
* 54ms per packet
* NOTES: Mode is finalized.


### MODE 2 - Short Range (10417 bps)
* PWR = 6
* BW = 500
* SF = sf8
* CR = 4/6
* WDT = 1000                            
* Block Size = 128 bytes
* Max OTA Size = 32768 bytes
* Max Requested Block Count = 32
* Data Rate = 10417 bps
* 112ms per packet
* NOTES: Mode is finalized.

### MODE 3 - Medium Range (2790 bps)
* PWR = 12
* BW = 500
* SF = sf10
* CR = 4/7
* WDT = 2000                            
* Block Size = 128 bytes
* Max OTA Size = 32768
* Max Requested Block Count = 32
* Data Rate = 2790 bps
* 414ms per packet
* NOTES: May chose 250 over 500 for BW?  Needs testing.

### MODE 4 - Long Range (366 bps)
* PWR = 17
* BW = 250
* SF = sf12
* CR = 4/8
* WDT = 5000                            
* Block Size = 64 bytes
* Max OTA Size = 16384
* Max Requested Block Count = 16
* Data Rate = 366 bps
* 2036ms per packet
* NOTES: Test WDT before finalizing.

### MODE 5 - Maximum Range for Emergency Use (183 bps hardware minimum)
* PWR = 20
* BW = 125
* SF = sf12
* CR = 4/8
* WDT = 5000                            
* Block Size = 32 bytes
* Max Requested Block Count = 8
* Max OTA Size = 8192
* Data Rate = 183 bps
* 2499ms per packet
* NOTES: Test WDT before finalizing.


## LMODEM Channels
1. 913 MHz
2. 914 MHz
3. 915 MHz
4. 916 MHz
5. 917 MHz 