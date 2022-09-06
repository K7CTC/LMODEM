import base64
import textwrap
import lzma
from hashlib import blake2b

# first we want to get a secure hash of the source file
# for this project I will be using the BLAKE2 hash algorythm with a message digest size of 32 bytes
with open('input.jpg', 'rb') as input_file:
    secure_hash = blake2b(digest_size=32)
    secure_hash.update(input_file.read())


# with open('input.heic', 'rb') as input_file:
#     b64_bytes = base64.b64encode(input_file.read())



# b64_bytes_compressed = lzma.compress(b64_bytes)
# del b64_bytes

# hex_string_compressed = b64_bytes_compressed.hex()
# del b64_bytes_compressed


# blocks = textwrap.wrap(hex_string_compressed, 256)
# del hex_string_compressed

# print(blocks[0])
# print(type(blocks[0]))


# # SIMULATE DATA TRANSFER BY ITERATING THROUGH PACKETS
# for block in blocks:
#     index = blocks.index(block)
#     print(str(index) + ',' + block)

# # REBUILD FILE ON THE "OTHER END"
# received_hex_string_compressed = ''
# for received_block in blocks:
#     received_hex_string_compressed = received_hex_string_compressed + received_block

# del blocks

# received_b64_bytes_compressed = bytes.fromhex(received_hex_string_compressed)
# del received_hex_string_compressed

# received_b64_bytes_decompressed = lzma.decompress(received_b64_bytes_compressed)
# del received_b64_bytes_compressed

# with open('output.heic', 'wb') as file:
#     file.write(base64.b64decode(received_b64_bytes_decompressed))
