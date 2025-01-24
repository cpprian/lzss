import argparse
from typing import Final, Optional, Tuple
from bitarray import bitarray
from utils import read_data, write_data


MATCH_LENGTH_MASK: Final[int] = 0xF
WINDOW_SIZE: Final[int] = 0xFFF
IS_MATCH_BIT: Final[bool] = True
LENGTH_OFFSET: Final[int] = 2


def extract_repeat(x: bytes, num_bytes: int) -> bytes:
    repetitions, remainder = divmod(num_bytes, len(x))
    return x * repetitions + x[:remainder]


def find_duplicate(data: bytes, current_position: int) -> Optional[Tuple[int, int]]:
    end_of_buffer = min(current_position + MATCH_LENGTH_MASK + LENGTH_OFFSET, len(data))
    search_start = max(0, current_position - WINDOW_SIZE)
    match_indices = [
        i
        for i in range(search_start, current_position)
        if data[i] == data[current_position]
    ]

    for search_position in match_indices:
        match_length = 0
        while (
            current_position + match_length < end_of_buffer
            and data[search_position + match_length] == data[current_position + match_length]
            and match_length < MATCH_LENGTH_MASK
        ):
            match_length += 1

        if match_length >= 3:
            return current_position - search_position, match_length


def compress(data_path: str, output_path: str = None, file_type: bool = False) -> bytes:
    data = read_data(data_path, file_type)
    output_buffer = bitarray(endian="big")

    i = 0
    while i < len(data):
        if match := find_duplicate(data, i):
            match_distance, match_length = match
            print(f"id: {i}, match: {match_distance}, length: {match_length}")
            output_buffer.append(IS_MATCH_BIT)
            dist_hi, dist_lo = match_distance >> 4, match_distance & 0xF
            output_buffer.frombytes(bytes([dist_hi, (dist_lo << 4) | (match_length - LENGTH_OFFSET)]))
            i += match_length
        else:
            output_buffer.append(not IS_MATCH_BIT)
            output_buffer.frombytes(bytes([data[i]]))
            i += 1

    output_buffer.fill()

    write_data(output_buffer, output_path)


def main():
    parser = argparse.ArgumentParser(description="LZSS compression tool")
    parser.add_argument("input_file", help="Input file path")
    parser.add_argument("--output_file", help="Output file path")
    parser.add_argument(
        "--file_type",
        choices=["image", "auto"],
        default="auto",
        help="File type (default: auto-detect)",
    )
    args = parser.parse_args()

    compress(args.input_file, args.output_file, args.file_type)


if __name__ == "__main__":
    main()
