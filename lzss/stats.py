import argparse
import matplotlib.pyplot as plt
from collections import Counter
import math
import os

#Obliczenie entropi i wyznaczenie histogramów dla danych wejściowych
#wyniki zapisywane są w katalogu histograms

def compute_histogram(data: bytes) -> dict:
    return dict(Counter(data))

def compute_entropy(data: bytes) -> float:
    histogram = compute_histogram(data)

    total_symbols = len(data)

    entropy = 0
    for count in histogram.values():
        probability = count / total_symbols
        entropy -= probability * math.log2(probability)
    
    return entropy

def plot_histogram(histogram: dict, entropy: float, file_name: str):
    byte_values = list(histogram.keys())
    frequencies = list(histogram.values())

    plt.figure(figsize=(12, 8))
    plt.bar(byte_values, frequencies, color='blue', edgecolor='black', width=1.0)
    plt.title(f"Plik: {file_name} | Entropia: {entropy:.4f} bitów\nHistogram", fontsize=16)
    plt.xlabel("Wartość (0-255)", fontsize=14)
    plt.ylabel("Częstotliwość", fontsize=14)
    plt.xticks(range(0, 256, 25))
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    output_file = f"histograms/{os.path.splitext(file_name)[0]}.png"
    plt.savefig(output_file, dpi=300)
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Compute histogram and entropy of a file.")
    parser.add_argument("file_path", help="Path to the input file")
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
    entropy = compute_entropy(data)

    plot_histogram(histogram, entropy, os.path.basename(args.file_path))

if __name__ == "__main__":
    main()
