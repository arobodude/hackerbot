import lz4.frame
import lz4framed
from lz4framed import Decompressor
import binascii
import struct

with open('test_data.txt', 'r') as file:
    hex_data = file.read().strip()


def parse_hex_value(hex_data, current_index, size=8, is_float=False, lsb=True):
    hex_value = hex_data[current_index:current_index + size]
    if lsb:
        # Reverse byte order if LSB
        hex_value = ''.join(hex_value[i:i + 2] for i in range(0, size, 2)[::-1])

    # Convert to integer or float
    if is_float:
        parsed_value = struct.unpack('!f', bytes.fromhex(hex_value))[0]  # Parse as float
    else:
        parsed_value = int(hex_value, 16)  # Parse as int

    # Update current index
    new_index = current_index + size

    return parsed_value, new_index

def parse_hex_data(hex_data):
    current_index = 0
    id, current_index = parse_hex_value(hex_data, current_index, size=4)
    size, current_index = parse_hex_value(hex_data, current_index, size=8)
    lz4_size, current_index = parse_hex_value(hex_data, current_index, size=8)
    width, current_index = parse_hex_value(hex_data, current_index, size=8)
    height, current_index = parse_hex_value(hex_data, current_index, size=8,)

    resolution, current_index = parse_hex_value(hex_data, current_index, size=8, is_float=True)
    origin_x, current_index = parse_hex_value(hex_data, current_index, size=8, is_float=True)
    origin_y, current_index = parse_hex_value(hex_data, current_index, size=8, is_float=True)

    lz4_compressed_data = hex_data[current_index:]

    return {
        "id": id,
        "size": size,
        "lz4_size": lz4_size,
        "width": width,
        "height": height,
        "resolution": resolution,
        "origin_x": origin_x,
        "origin_y": origin_y,
        "lz4_compressed_data": lz4_compressed_data
    }

parsed_data = parse_hex_data(hex_data)

# Display parsed values
for key, value in parsed_data.items():
    print(f"{key}: {value}")

print(len(parsed_data['lz4_compressed_data']) / 2)

original_bytes = bytes.fromhex(parsed_data['lz4_compressed_data'])
lsb_bytes = original_bytes[::-1]

with open('msb', 'wb') as f:
    f.write(original_bytes)

with open('lsb', 'wb') as f:
    f.write(lsb_bytes)

def decompress_lz4(byte_data):
    with open(byte_data, 'rb') as f:
        try:
            for chunk in Decompressor(f):
                print(chunk)
                #decoded.append(chunk)
        except Lz4FramedNoDataError as e:
            print(f"Decompression failed: {e}")

    # try:
    #     # Decompress using LZ4
    #     decompressed_data = lz4framed.decompress(byte_data)
    #     print(f"Decompressed data: {decompressed_data}")
    #     return decompressed_data
    # except RuntimeError as e:
    #     print(f"Decompression failed: {e}")

# Test decompression with original (MSB) and reversed (LSB) byte order
print("Testing MSB order:")
decompress_lz4("msb")

print("Testing LSB order:")
decompress_lz4("lsb")

