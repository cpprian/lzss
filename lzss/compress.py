import argparse
from typing import Final, Optional, Tuple
from bitarray import bitarray
from lzss.utils import read_data, write_data


MATCH_LENGTH_MASK: Final[int] = 15
WINDOW_SIZE: Final[int] = 4096
IS_MATCH_BIT: Final[bool] = 1
LENGTH_OFFSET: Final[int] = 3
LOOKUP_SIZE: Final[int] = 18


def extract_repeat(x: bytes, num_bytes: int) -> bytes:
    repetitions, remainder = divmod(num_bytes, len(x))
    return x * repetitions + x[:remainder]


def find_duplicate(data: bytes, current_position: int) -> Optional[Tuple[int, int]]:
    end_of_buffer = min(current_position + MATCH_LENGTH_MASK + LENGTH_OFFSET, len(data))
    search_start = max(0, current_position - WINDOW_SIZE)

    for match_candidate_end in range(
        end_of_buffer, current_position + LENGTH_OFFSET + 1, -1
    ):
        match_candidate = data[current_position:match_candidate_end]
        potential_matches = (
            (
                current_position - search_position,
                extract_repeat(
                    data[search_position:current_position], len(match_candidate)
                ),
            )
            for search_position in range(search_start, current_position)
        )

        match = next(filter(lambda x: x[1] == match_candidate, potential_matches), None)
        if match:
            return match[0], len(match_candidate)

    return None


def compress(data_path: str, output_path: str = None, file_type: bool = False) -> bytes:
    data = read_data(data_path, file_type)
    output_buffer = bitarray(endian="big")

    i = 0
    while i < len(data):
        if match := find_duplicate(data, i):
            match_distance, match_length = match
            output_buffer.append(IS_MATCH_BIT)
            dist_hi, dist_lo = (
                match_distance >> 4,
                (match_distance) & MATCH_LENGTH_MASK,
            )
            output_buffer.frombytes(
                bytes([dist_hi, (dist_lo << 4) | (match_length - LENGTH_OFFSET)])
            )
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
