import base64
import re
import textwrap
import lzma
from rich import print



with open('jt_strng.xm', 'rb') as input_file:
    b64_bytes = base64.b64encode(input_file.read())

b64_bytes_compressed = lzma.compress(b64_bytes)
del b64_bytes

hex_string_compressed = b64_bytes_compressed.hex()
del b64_bytes_compressed

blocks = textwrap.wrap(hex_string_compressed, 256)
del hex_string_compressed

print(len(blocks))

#create dictionary for storage on the other end
received_blocks = {block: '' for block in range(len(blocks))}

print(received_blocks)
print(len(received_blocks))

# for block in blocks:
#     received_blocks[blocks.index(block)] = block

# #mess up the data
# received_blocks[7] = ''
# received_blocks[13] = ''
# received_blocks[20] = ''



# print(received_blocks)
# print(len(received_blocks))

# missing_blocks = ''

# for block in received_blocks:
#     if received_blocks[block] == '':
#          missing_blocks = missing_blocks + str(block) + '|'

# if len(missing_blocks) != 0:
#     missing_blocks = missing_blocks.rstrip(missing_blocks[-1])


# print(missing_blocks)




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
