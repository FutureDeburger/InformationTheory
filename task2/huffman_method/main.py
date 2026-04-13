import heapq


class HuffmanNode:
    def __init__(self, prob, symbol=None, left=None, right=None):
        self.prob = prob
        self.symbol = symbol
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.prob < other.prob


def build_huffman_tree(symbols, probs):
    heap = []
    for sym, p in zip(symbols, probs):
        heapq.heappush(heap, HuffmanNode(p, sym))

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        parent = HuffmanNode(left.prob + right.prob, left=left, right=right)
        heapq.heappush(heap, parent)

    return heap[0]


def generate_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}

    if node.symbol is not None:
        codebook[node.symbol] = prefix
    else:
        generate_codes(node.left, prefix + "0", codebook)
        generate_codes(node.right, prefix + "1", codebook)

    return codebook


def huffman_encode(message, codebook):
    return ''.join(codebook[ch] for ch in message)


def huffman_decode(encoded_string, root):
    decoded = []
    node = root
    for bit in encoded_string:
        if bit == '0':
            node = node.left
        else:
            node = node.right

        if node.symbol is not None:
            decoded.append(node.symbol)
            node = root
    return ''.join(decoded)


def read_alphabet(filename="alphabet.txt"):
    symbols = []
    probs = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split()
                if len(parts) >= 2:
                    symbols.append(parts[0])
                    probs.append(float(parts[1]))
    return symbols, probs


def read_message(filename="input.txt"):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read().strip()


def huffman_main():
    symbols, probs = read_alphabet("alphabet.txt")
    message = read_message("input.txt")

    root = build_huffman_tree(symbols, probs)
    codebook = generate_codes(root)

    encoded = huffman_encode(message, codebook)
    decoded = huffman_decode(encoded, root)

    with open("output_1.txt", "w", encoding="utf-8") as f:
        f.write("Код Хаффмана\n")
        f.write("Кодовая таблица:\n")
        for sym in symbols:
            f.write(f"  '{sym}': {codebook[sym]}\n")
        f.write(f"\nИсходное сообщение: {message}\n")
        f.write(f"Закодированное сообщение: {encoded}\n")
        f.write(f"Декодированное сообщение: {decoded}\n")
        f.write(f"Длина кода: {len(encoded)} бит\n")

    print("Результат записан в output_1.txt")
    return codebook, encoded


if __name__ == "__main__":
    huffman_main()