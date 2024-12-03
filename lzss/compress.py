import argparse


def add(a, b):
    return a + b


def main():
    parser = argparse.ArgumentParser(description="LZSS compression tool")
    parser.add_argument("input_file", help="Input file path")
    parser.add_argument("output_file", help="Output file path")
    args = parser.parse_args()

    print(f"Input file: {args.input_file}\nOutput file: {args.output_file}")


if __name__ == "__main__":
    main()
