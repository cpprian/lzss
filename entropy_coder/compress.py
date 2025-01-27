from collections import Counter, defaultdict
import heapq
import os

from entropy_coder.huffman import HuffmanNode


def process_files(input_files, output_folder, analysis_file):
    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)

    with open(analysis_file, "w") as analysis:
        analysis.write("File Compression Analysis\n")
        analysis.write("==========================\n\n")

        for input_file in input_files:
            try:
                with open(input_file, "rb") as f:
                    data = f.read()

                original_size = len(data)

                # Perform Huffman Encoding
                encoded_data, codebook = huffman_encode(data)
                encoded_bytes = int(encoded_data, 2).to_bytes((len(encoded_data) + 7) // 8, byteorder="big")

                # Define output paths
                file_name = os.path.basename(input_file)
                output_path = os.path.join(output_folder, file_name.replace("_compressed.bin", "_huffman.bin"))
                codebook_path = output_path + ".codebook"

                # Save compressed data
                with open(output_path, "wb") as f:
                    f.write(encoded_bytes)

                # Save codebook
                with open(codebook_path, "w") as f:
                    for symbol, code in codebook.items():
                        f.write(f"{symbol}:{code}\n")

                compressed_size = len(encoded_bytes)

                # Write analysis for this file
                compression_ratio = original_size / compressed_size if compressed_size > 0 else 0
                analysis.write(f"File: {file_name}\n")
                analysis.write(f"Original size: {original_size} bytes\n")
                analysis.write(f"Compressed size: {compressed_size} bytes\n")
                analysis.write(f"Compression ratio: {compression_ratio:.2f}\n\n")

                print(f"Processed {file_name}: Compressed and saved to {output_path}.")

            except Exception as e:
                print(f"Error processing {input_file}: {e}")
                analysis.write(f"File: {input_file} - Error: {e}\n\n")


def build_huffman_tree(data):
    frequency = Counter(data)
    priority_queue = [HuffmanNode(symbol, freq) for symbol, freq in frequency.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = HuffmanNode(frequency=left.frequency + right.frequency)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)

    return priority_queue[0] if priority_queue else None


def build_huffman_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}

    if node.symbol is not None:
        codebook[node.symbol] = prefix
    else:
        if node.left:
            build_huffman_codes(node.left, prefix + "0", codebook)
        if node.right:
            build_huffman_codes(node.right, prefix + "1", codebook)

    return codebook


def huffman_encode(data):
    tree = build_huffman_tree(data)
    codebook = build_huffman_codes(tree)

    encoded_data = "".join(codebook[byte] for byte in data)
    return encoded_data, codebook


def main():
    input_files = [
        "lzss_compressed/boat_compressed.bin",
        "lzss_compressed/chronometer_compressed.bin",
        "lzss_compressed/lorem_compressed.bin",
        "lzss_compressed/mandril_compressed.bin",
        "lzss_compressed/peppers_compressed.bin",
    ]

    output_folder = "entropy_compressed"
    analysis_file = os.path.join(output_folder, "compression_analysis.txt")

    process_files(input_files, output_folder, analysis_file)


if __name__ == "__main__":
    main()
