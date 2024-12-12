import argparse
from typing import Final, Optional, Tuple
from bitarray import bitarray
from lzss.utils import read_data, write_data

IS_MATCH_BIT: Final[bool] = 1
LENGTH_OFFSET: Final[int] = 2
MATCH_LENGTH_MASK: Final[int] = 15

def decompress(input_path: str, output_path: str) -> bytes:
    compressed_bytes = read_data(input_path)
    data = bitarray(endian="big")
    data.frombytes(compressed_bytes)
    assert data, f"Cannot decompress {compressed_bytes}"


    output_buffer = bytearray()

    while len(data) >= 9:
        if data.pop(0) != IS_MATCH_BIT:
            byte = data[:8].tobytes()
            del data[:8]
            output_buffer.extend(byte)
        else:
            hi, lo = data[:16].tobytes()
            del data[:16]
            distance = (hi << 4) | (lo >> 4)
            length = (lo & MATCH_LENGTH_MASK) + LENGTH_OFFSET
            for _ in range(length):
                output_buffer.append(output_buffer[-distance])

    try:
        if output_path is None:
            output_path = "default_output_path"

        with open(output_path, "wb") as f:
            f.write(bytes(output_buffer))
    except Exception as e:
        print(f"Error: Can't create file {output_path}. {e}")


def main():
    parser = argparse.ArgumentParser(description="LZSS compression tool")
    parser.add_argument("input_file", help="Compressed file path")
    parser.add_argument("--output_file", help="Decempressed file path")

    args = parser.parse_args()

    decompress(args.input_file, args.output_file)


if __name__ == "__main__":
    main()

