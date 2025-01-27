from collections import Counter, defaultdict
import heapq
import os


class HuffmanNode:
    def __init__(self, symbol=None, frequency=0):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency


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


def huffman_decode(encoded_data, codebook):
    reverse_codebook = {v: k for k, v in codebook.items()}
    decoded_data = []

    buffer = ""
    for bit in encoded_data:
        buffer += bit
        if buffer in reverse_codebook:
            decoded_data.append(reverse_codebook[buffer])
            buffer = ""

    return bytes(decoded_data)


def main():
    input_path = "lzss_compressed/boat_compressed.bin"
    output_path = "entropy_compressed/boat_huffman.bin"

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(input_path, "rb") as f:
        data = f.read()

    original_size = len(data)

    encoded_data, codebook = huffman_encode(data)

    encoded_bytes = int(encoded_data, 2).to_bytes((len(encoded_data) + 7) // 8, byteorder="big")

    with open(output_path, "wb") as f:
        f.write(encoded_bytes)

    codebook_path = output_path + ".codebook"
    with open(codebook_path, "w") as f:
        for symbol, code in codebook.items():
            f.write(f"{symbol}:{code}\n")

    compressed_size = len(encoded_bytes)

    analysis_path = os.path.join(os.path.dirname(output_path), "compression_analysis.txt")
    with open(analysis_path, "w") as f:
        f.write(f"Original file size: {original_size} bytes\n")
        f.write(f"Compressed file size: {compressed_size} bytes\n")
        compression_ratio = original_size / compressed_size if compressed_size > 0 else 0
        f.write(f"Compression ratio: {compression_ratio:.2f}\n")

    print(f"Huffman compression completed. Output saved to {output_path}.")
    print(f"Codebook saved to {codebook_path}.")
    print(f"Analysis saved to {analysis_path}.")


if __name__ == "__main__":
    main()
