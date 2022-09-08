import base64
from base64 import b85encode, b85decode
import re
import textwrap
import lzma
from rich import print
from pathlib import Path
from hashlib import blake2b

print()
print()


#obtain secure hash for source file
with open('jt_strng.xm', 'rb') as file:
    input_file_secure_hash = blake2b(digest_size=32)
    input_file_secure_hash.update(file.read())
print(f'Input File Secure Hash: {input_file_secure_hash.hexdigest()}')

#get size of source file (in bytes)
file_size = Path('jt_strng.xm').stat().st_size
print(f'Input File Size: {file_size}')

#compress source file
with open('jt_strng.xm', 'rb') as file:
    input_file_compressed = lzma.compress(file.read())
print(f'Input File Compressed: {len(input_file_compressed)}')

#base64 encode compressed source file
input_file_compressed_b85 = b85encode(input_file_compressed)
print(f'Input File Compressed Base85: {len(input_file_compressed_b85)}')

input_file_compressed_b85_hex = input_file_compressed_b85.hex()
print(f'Input File Compressed Base85 Hexadecimal: {len(input_file_compressed_b85_hex)}')

input_blocks = textwrap.wrap(input_file_compressed_b85_hex, 256)
print(f'Input File Compressed Base85 Hexadecimal 128 byte blocks: {len(input_blocks)}')


print()
print()

print('"Data Transfer Happens Here"')

print()
print()

# # SIMULATE DATA TRANSFER BY ITERATING THROUGH PACKETS
# for block in blocks:
#     index = blocks.index(block)
#     print(str(index) + ',' + block)

# REBUILD FILE ON THE "OTHER END"
output_file_compressed_b85_hex = ''
for received_block in input_blocks:
    output_file_compressed_b85_hex = output_file_compressed_b85_hex + received_block

#decode from hex
output_file_compressed_b85 = bytes.fromhex(output_file_compressed_b85_hex)

#decode from b85
output_file_compressed = b85decode(output_file_compressed_b85)

#decompress
output_file = lzma.decompress(output_file_compressed)

#write to disk
with open('output.xm', 'wb') as file:
    file.write(output_file)



#obtain secure hash for new file
with open('output.xm', 'rb') as file:
    output_file_secure_hash = blake2b(digest_size=32)
    output_file_secure_hash.update(file.read())
print(f'Output File Secure Hash: {output_file_secure_hash.hexdigest()}')

print(f' Input File Secure Hash: {input_file_secure_hash.hexdigest()}')














# #create dictionary for storage on the other end
# received_blocks = {block: '' for block in range(len(blocks))}

# print(received_blocks)
# print(len(received_blocks))

# # for block in blocks:
# #     received_blocks[blocks.index(block)] = block

# # #mess up the data
# # received_blocks[7] = ''
# # received_blocks[13] = ''
# # received_blocks[20] = ''



# # print(received_blocks)
# # print(len(received_blocks))

# # missing_blocks = ''

# # for block in received_blocks:
# #     if received_blocks[block] == '':
# #          missing_blocks = missing_blocks + str(block) + '|'

# # if len(missing_blocks) != 0:
# #     missing_blocks = missing_blocks.rstrip(missing_blocks[-1])


# # print(missing_blocks)
