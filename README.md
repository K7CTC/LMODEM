# LMODEM

LMODEM is the world's first file transfer protocol designed specifically for [LoRa](https://en.wikipedia.org/wiki/LoRa).  Its name is a throwback to X, Y, and [ZMODEM](https://en.wikipedia.org/wiki/ZMODEM) which I used heavily back when I was a [BBS](https://en.wikipedia.org/wiki/Bulletin_board_system) SysOp.  Use it to transfer arbitrary files up to 32kb in size over distances in excess of 20mi.

## Why?

The short answer, I was just curious to see if it was possible.

I thought it would be a neat hack to send arbitrary files over LoRa, a technology not intended for such a use case.  After searching the internet I was unable to find any discussion or examples of anyone else attempting this feat.  So, I decided to take up the challenge myself.

LMODEM serves as a learning exercise in how to design a file transfer protocol from scratch.  It is also a fully functional utility for reliably transferring files over LoRa.

## Features

- [BLAKE2b](http://www.blake2.net) secure hash algorithm provides 100% confidence in transferred files.
- [Lempel-Ziv Markov chain Algorithm (LZMA)](https://en.wikipedia.org/wiki/Lempel–Ziv–Markov_chain_algorithm) compression significantly reduces "over the air" file size.
- Resume partial/interrupted transfers with unlimited retries.
- LMODEM "channels" simplify frequency selection.
- LMODEM "modes" simplify LoRa settings selection.
- Automatic LoStik detection and configutation.

## Constraints

- Maximum file name length of 32 characters.
- Maximim compressed (over the air) file size of 32,768 bytes.

## Requirements

- [Python 3.10+](https://www.python.org)
  - [pyserial 3.5+ (via pip)](https://pypi.org/project/pyserial/)
  - [rich 12.6.0+ (via pip)](https://pypi.org/project/rich/)
- [Ronoth LoStik](https://ronoth.com/products/lostik)

## Basic Usage

    usage: lmodem.py [-h] (-s filename | -r) [-c {1,2,3,4,5}] [-m {1,2,3,4,5}]

    LMODEM

    optional arguments:
    -h, --help              show this help message and exit
    -s filename, --send filename
                            send the specified file
    -r, --receive           receive an incoming file
    -c {1,2,3,4,5}, --channel {1,2,3,4,5}
                            LMODEM channel (default: 3)
    -m {1,2,3,4,5}, --mode {1,2,3,4,5}
                            LMODEM mode (default: 2)

## LMODEM Channels

#### Channel 1 - 913 MHz
#### Channel 2 - 914 MHz
#### Channel 3 - 915 MHz
#### Channel 4 - 916 MHz
#### Channel 5 - 917 MHz 

## Channel Selection

The 902-928 MHz ISM band (aka [33cm](https://en.wikipedia.org/wiki/33-centimeter_band)) is allocated for amateur radio use on a secondary basis.  As such, it is shared with many unlicensed devices operating with various modulation methods.  Short of having an SDR with waterfall display, monitoring 33cm for a "clear" frequency is simply not an option.  Choosing an operating frequency for LoRa is done blindly.  In my testing, the default channel of 915Mhz (center of band) has worked 100% of the time.  

If there are multiple pairs of LOMODEM stations, perhaps supporting an event.  Then coordination should occur to ensure each station pair uses a dedicated channel.

If communication difficulty occurs, it could be due to interference on the selected channel.  In this case, try again using a different channel.

## LMODEM Modes

#### Mode 1 - Minimum Range (Bench Testing Only)
- Transmit Power = 3.0dBm/2.0mW/42.6mA
- Bandwidth = 500 KHz
- Spreading Factor = 9
- Coding Rate = 4/6
- Watchdog Timer Time-Out = 1000 ms                           
- Block Size = 128 bytes
- Max OTA File Size = 32,768 bytes
- Data Rate = 5.86 kbps
- Packet Air Time = 199 ms
#### Mode 2 - Short Range
- Transmit Power = 7.0dBm/5.0mW/52.0mA
- Bandwidth = 250 KHz
- Spreading Factor = 10
- Coding Rate = 4/7
- Watchdog Timer Time-Out = 2000 ms                           
- Block Size = 128 bytes
- Max OTA File Size = 32,768 bytes
- Data Rate = 1.4 kbps
- Packet Air Time = 828 ms
#### Mode 3 - Medium Range
- Transmit Power = 13.0dBm/20.0mW/78.0mA
- Bandwidth = 250 KHz
- Spreading Factor = 11
- Coding Rate = 4/8
- Watchdog Timer Time-Out = 3000 ms                           
- Block Size = 128 bytes
- Max OTA File Size = 32,768 bytes
- Data Rate = 671 bps
- Packet Air Time = 2066 ms
#### Mode 4 - Long Range
- Transmit Power = 17.0dBm/50.1mW/103.6mA
- Bandwidth = 250 KHz
- Spreading Factor = 12
- Coding Rate = 4/8
- Watchdog Timer Time-Out = 4000 ms                           
- Block Size = 64 bytes
- Max OTA File Size = 16,384 bytes
- Data Rate = 366 bps
- Packet Air Time = 2036 ms
#### Mode 5 - Maximum Range (Emergency Use Only)
- Transmit Power = 18.5dBm/70.8mW/124.4mA
- Bandwidth = 125 KHz
- Spreading Factor = 12
- Coding Rate = 4/8
- Watchdog Timer Time-Out = 7500 ms                           
- Block Size = 32 bytes
- Max OTA File Size = 8,192 bytes
- Data Rate = 183 bps
- Packet Air Time = 2499 ms

## Mode Selection

From the Amateur Radio General Class question pool (G1C04 (A) [97.313(a)]):
- Q. Which of the following limitations apply to transmitter power on **every** amateur band?
- A. Only the minimum power necessary to carry out the desired communications should be used.

Along those lines, I crafted LMODEM modes with progressively more robust settings, including transmit power.  There is obviously a trade off between range and speed for each mode.  As a best practice (and for optimal transfer speed) choose the lowest mode that ensures reliable communication.  Use your best judgement on which mode to start with, then move higher if necessary.

## Basic Operation Overview

1. LMODEM is launced by both sending and receiving stations.  Order of execution does not matter.
2. A basic handshake is performed.
3. The sending station sends the file transfer details consisting of:
    1. name
    2. size in bytes (on disk)
    3. size in bytes (over the air)
    4. block count
    5. secure hash hex digest
4. The receiving station processes the file transfer details then instructs the sending station how to proceed:
    1. Duplicate file found. Integrity check passed. (exit)
    2. Duplicate filename found. Integrity check failed! (abort)
    3. Start file transfer. (send the whole file)
    4. Resume file transfer. (send only the requested blocks)
5. The sending station responds accordingly by either...
    1. exiting gracefully.
    2. aborting the transfer.
    3. sending all file blocks.
    4. sending only the requested file blocks.
6. The sending station sends an "end of transmission" packet.
7. The receiving station processes received blocks then responds eith either:
    1. File transfer incomplete. Try again to resume. (exit with warning)
    2. File transfer complete. Base85 decode failed! (exit with error)
    3. File transfer complete. Integrity check failed! (exit eith error)
    4. File transfer complete. Integrity check passed. (exit gracefully)
8. LMODEM execution is concluded on both sending and receiving stations.

Of course, the operational flow noted above assumes an uninterrupted transfer.  When the sending and receiving stations have difficulty communicating, alternate logic flows can occur.  These alternate flows are generally driven by the watchdog timer time-out setting.

## Handling Adverse Conditions

Generally speaking, when a time-out occurs (based on WDT setting), LMODEM will exit.  However, during block reception, up to five time-outs are allowed to occur before exiting.  This allows for minimal packet loss without aborting the entire transfer.

## Sending (file processing)

The file name to be sent (within the current working directory) is specified as a command line argument.  If the file name contains spaces, it must be wrapped in double quotes (e.g. "some file.ext").  If we were sending a file named example.csv using the default mode and channel we would launch LMODEM with the following command:

    lmodem.py -s example.csv

LMODEM then performs some initial checks against the file:
1. Check that the file actually exists.
2. Check if the file name exceeds LMODEM maximum of 32 characters.

If either of these checks fail, LMODEM will exit.

LMODEM then processes the file to be sent:
1. Generate the secure hash hex digest.
2. Compress the file.
3. Perform binary to text conversion using base85.
4. Determine size over the air in bytes.
5. Check if OTA size exceeds maximum for chosen mode. (exit if exceeds)
6. Determine size on dish in bytes.
7. Perform base85 to hexadecimal conversion.
8. Split resulting hexadecimal file into blocks sized for the chosen mode.
9. Obtain block count.

LMODEM then transforms the file blocks into packets by prepending the block index number to each block.  The resulting numbered packets are made available to the receiving station.

## Receiving (file processing)

To receive a file using the default mode and channel we would launch LMODEM with the following command:

    lmodem.py -r

The file name to be received is contained within the file transfer details.  LMODEM first uses this incoming file name to check if a file with matching name already exists within the current working directory.  If a file with a matching name is found, an integrity check is performed on it:

1. The secure hash hex digest is generated for the existing file and compared against that of the incoming file (using the file transfer details).
2. If the secure hash hex digests match, no work is performed and LMODEM exits gracefully.
3. If the secure hash hex digests do not match:
    1. Either the existing file is corrupted or a name collision has occurred.
    2. LMODEM exits with an error status.

In the absence of an existing matching file, LMODEM initializes an empty [Python dictionary](https://www.w3schools.com/python/python_dictionaries.asp) to temporarily store received file blocks.

LMODEM then checks for a "partial" file in the current working directory.  Partial files are stored in [prettyprinted](https://en.wikipedia.org/wiki/Prettyprint) [JSON](https://en.wikipedia.org/wiki/JSON) format and have the .json extension appended to the file name.  So a partial file for example.csv would habe the name of example.csv.json.  Partial files contain received blocks in key:value pairs where block index number is the key and the hexadecimal block is the value.  Partial files also contain the secure hash hex digest of the source file.

If a partial file is found, it is parsed.  All available block data as well as secure hash hex digest are placed in the "received blocks" dictionary (initialized earlier).  Once the data has been transferred from disk to memory, the partial file is deleted from the file system.

LMODEM then determines whether to resume a partial transfer or start fresh.  This is accomplished by comparing the secure has hex digest obatined from the partial file against the incoming file tranfer details.  

#### If a match occurs, request missing blocks.

LMODEM compiles a list of missing block numbers by searching the "received blocks" dictionary for empty values.  When an empty value is found the block index number (key) is retrieved and added to a pipe delimeted string.

The string is then trimmed (from the right) based on the maximum request length (in charactes/bytes) for the chosen mode.  The maximum request length aligns closely with the packet size for the mode.  This is done so that the WDT is not triggered during transmit.  NOTE: This trimming operation limits the number of blocks that can be requested for the transfer operation.  For modes 1-3 the maximum request length is 127 bytes (or characters) which equates to 32 blocks.  For mode 4, the maximum request length is 63 bytes which equates to 16 blocks.  For mode 5, the maximum request length is 31 bytes which equates to 8 blocks.  If the maximum request length is not exceeded, all missing blocks are requested.

Next, LMODEM calculates the number of received blocks and prepends this value the missing block numbers string.  This string now represents the "block request details" and is transmitted to the sending station for processing.  Requested blocks are then received and added to the received blocks dictionary.  Rinse and repeat as necessary.

#### If a match does not occur, request all blocks. (start new transfer)

LMODEM purges all existing data from the "received blocks" dictionary.  The dictionary is then initialized by pre-populating keys (block index numbers) with empty values based on the block count from the file transfer details.  To start a new transfer, a special "block request details" packet is formed containing "000000" then transmitted to the sending station for processing.  When the sending station sees that 0 blocks have been received, it knows to send all blocks.

NOTE: The sending station only reads the first three characters (the received block count) and discards the remaining three characters.  LoRa struggles with extremely short packet sizes, so this is a special case where the packet is padded with extra zeros to improve the odds of reception and proper decoding.

One of two conditions will cause LMODEM to stop listening for additional file block packets:

1. An "end of transmission" packet is received.
2. The LoStik watchdog timer time-out is triggered five times.

At this point the received blocks are processed.  LMODEM counts the number of received blocks and compares it to the block count from the incoming file transfer details.

#### If all blocks have been received, process file.

1. All hexadecimal block values from the "received blocks" dictionary are concatenated back into a contiguous blob (string).  
2. Hexadecimal string is converted to base85.
3. Attempt text to binary conversion from base85.  Exit upon error.
4. Decompress file (LZMA).
5. Write file to disk (using file name from transfer details).
6. Generate secure hash hex digest of received file as it resides in the file system.
7. Compare the secure hash hex digest from the file transfer details against that of the received file.
    1. If the secure hash hex digests do not match, the received file is deleted.  LMODEM will exit with an error.
    2. If the secure hash hex digests do match, the transfer is complete and LMODEM exits gracefully.

#### If some blocks are missing, process partial file.

LMODEM appends the expected secure hash hex digest from the file transfer details to the received blocks dictionary.  The dictionary is then converted into prettyprinted json and written to disk.  The .json file name extension is used to denote a partial file.

## Appendix

- [Microchip RN2903 LoRa Module - Data Sheet](https://ww1.microchip.com/downloads/aemDocuments/documents/WSG/ProductDocuments/DataSheets/RN2903-Low-Power-Long-Range-LoRa-Technology-Transceiver-Module-DS50002390K.pdf)
- [Microchip RN2903 LoRa Module - Command Reference](https://ww1.microchip.com/downloads/en/DeviceDoc/RN2903%20LoRa%20Technology%20Module%20Command%20Reference%20User%20Guide-40001811B.pdf)