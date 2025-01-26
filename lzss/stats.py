import argparse
import matplotlib.pyplot as plt
from collections import Counter
import math
import os

# Obliczenie entropii i wyznaczenie histogramów dla danych wejściowych
# Wyniki zapisywane są w katalogu histograms

def compute_histogram(data: bytes) -> dict:
    return dict(Counter(data))


def compute_block_entropy(data: bytes, block_order: int) -> float:
    block_size = block_order + 1
    blocks = [tuple(data[i:i + block_size]) for i in range(len(data) - block_size + 1)]
    histogram = Counter(blocks)

    total_blocks = len(blocks)
    entropy = 0
    for count in histogram.values():
        probability = count / total_blocks
        entropy -= probability * math.log2(probability)
    return entropy


def compute_average_bit_length(output_path: str, input_data: bytes) -> float:
    file_size_bits = os.path.getsize(output_path) * 8  # File size in bits
    num_symbols = len(input_data)  # Number of symbols (bytes)
    avg_bit_length = file_size_bits / num_symbols  # Average bit length
    return avg_bit_length


def plot_histogram(histogram: dict, entropy: float, file_name: str, order: int):
    byte_values = list(histogram.keys())
    frequencies = list(histogram.values())

    plt.figure(figsize=(12, 8))
    plt.bar(byte_values, frequencies, color='blue', edgecolor='black', width=1.0)
    plt.title(f"Plik: {file_name} | Entropia (rząd {order}): {entropy:.4f} bitów\nHistogram", fontsize=16)
    plt.xlabel("Wartość (0-255)", fontsize=14)
    plt.ylabel("Częstotliwość", fontsize=14)
    plt.xticks(range(0, 256, 25))
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    output_dir = "histograms"
    os.makedirs(output_dir, exist_ok=True)
    output_file = f"{output_dir}/{os.path.splitext(file_name)[0]}_order_{order}.png"
    plt.savefig(output_file, dpi=300)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Compute histogram, entropy, and average bit length of a file.")
    parser.add_argument("file_path", help="Path to the input file")
    parser.add_argument("output_path", help="Path to the compressed output file (for average bit length calculation)")
    args = parser.parse_args()

    try:
        with open(args.file_path, "rb") as file:
            data = file.read()
    except FileNotFoundError:
        print(f"Error: File not found at path '{args.file_path}'")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    histogram = compute_histogram(data)

    # Calculate and display average bit length
    avg_bit_length = compute_average_bit_length(args.output_path, data)
    print(f"Average Bit Length: {avg_bit_length:.4f} bits/symbol")

    for order in range(1, 4):
        entropy = compute_block_entropy(data, order)
        print(f"Block Entropy (Order {order}): {entropy:.4f}")
        plot_histogram(histogram, entropy, os.path.basename(args.file_path), order)

    # dlaczego srednia dlugosc moze byc mniejsza? Np to dostalem dla pliku boat.pgm:
    #Average Bit Length: 8.1423 bits/symbol
    #Block Entropy (Order 1): 12.4920
    #Block Entropy (Order 2): 16.2987
    #Block Entropy (Order 3): 17.7583
    # glowna przyczyna moze byc to, ze kompresja wykorzystuje redundancje danych (identyfikuje powtarzajace sie wzorce)
    


if __name__ == "__main__":
    main()
