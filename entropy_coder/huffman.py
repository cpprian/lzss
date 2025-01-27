from collections import Counter, defaultdict
import heapq

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


if __name__ == "__main__":
    test_data = b"this is an example for huffman encoding"
    encoded, codes = huffman_encode(test_data)
    print("Encoded data:", encoded)
    print("Huffman Codes:", codes)

    decoded = huffman_decode(encoded, codes)
    print("Decoded data:", decoded)
