import math


def shannon_coding(symbols, probs):
    pairs = list(zip(symbols, probs))
    pairs.sort(key=lambda x: x[1], reverse=True)  # сортируем по убыванию вероятности

    sorted_symbols = [p[0] for p in pairs]
    sorted_probs = [p[1] for p in pairs]

    # print("После сортировки по убыванию:")
    # for sym, p in zip(sorted_symbols, sorted_probs):
    #     print(f"  {sym}: {p}")

    # Вычисление кумулятивных вероятностей q
    q = {}
    cumulative = 0.0

    for i, (sym, p) in enumerate(zip(sorted_symbols, sorted_probs)):
        q[sym] = cumulative
        cumulative += p

    # print("\nКумулятивные вероятности q:")
    # for sym in sorted_symbols:
    #     print(f"  {sym}: {q[sym]:.4f}")

    # Вычисление длин кодовых слов и самих кодов
    codebook = {}
    lengths = {}

    for i, (sym, p) in enumerate(zip(sorted_symbols, sorted_probs)):

        if p <= 0:
            length = 0
        else:
            length = math.ceil(-math.log2(p))
        lengths[sym] = length

        code = fractional_to_binary(q[sym], length)
        codebook[sym] = code

    return codebook, lengths, sorted_symbols, sorted_probs, q


def fractional_to_binary(fraction, num_bits):
    binary = ""
    x = fraction

    for _ in range(num_bits):
        x *= 2
        if x >= 1:
            binary += "1"
            x -= 1
        else:
            binary += "0"

    return binary


def shannon_encode(message, codebook):
    return ''.join(codebook[ch] for ch in message)


def shannon_decode(encoded_string, codebook_reverse, max_code_length=20):
    decoded = []
    i = 0

    while i < len(encoded_string):
        found = False
        for length in range(1, min(max_code_length, len(encoded_string) - i) + 1):
            candidate = encoded_string[i:i + length]
            if candidate in codebook_reverse:
                decoded.append(codebook_reverse[candidate])
                i += length
                found = True
                break

        if not found:
            raise ValueError(f"Не удалось декодировать на позиции {i}")

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


def shannon_main():
    symbols, probs = read_alphabet("alphabet.txt")
    message = read_message("input.txt")

    codebook, lengths, sorted_symbols, sorted_probs, q = shannon_coding(symbols, probs)

    encoded = shannon_encode(message, codebook)

    reverse_codebook = {v: k for k, v in codebook.items()}
    decoded = shannon_decode(encoded, reverse_codebook)

    avg_length = sum(lengths[sym] * prob for sym, prob in zip(symbols, probs))
    entropy = -sum(p * math.log2(p) for p in probs if p > 0)

    with open("output_2.txt", "w", encoding="utf-8") as f:  # 'a' - append (добавление к файлу)
        f.write("Код Шеннона\n")
        f.write("\nТаблица кодов:\n")
        for sym in symbols:
            f.write(f"  '{sym}': {codebook[sym]} "
                    # f"(длина: {lengths[sym]}, p={probs[symbols.index(sym)]})\n"
                    f"\n")

        # f.write("\nПромежуточные вычисления (после сортировки):\n")
        # for sym, p, q_val in zip(sorted_symbols, sorted_probs, [q[s] for s in sorted_symbols]):
        #     f.write(f"  {sym}: p={p}, q={q_val:.4f}, длина={lengths[sym]}, код={codebook[sym]}\n")

        f.write(f"\nИсходное сообщение: {message}\n")
        f.write(f"Закодированное сообщение: {encoded}\n")
        f.write(f"Декодированное сообщение: {decoded}\n")
        f.write(f"Длина кода: {len(encoded)} бит\n")
        # f.write(f"Средняя длина кода: {avg_length:.4f} бит/символ\n")
        # f.write(f"Энтропия источника: {entropy:.4f} бит/символ\n")
        # f.write(f"Избыточность: {avg_length - entropy:.4f} бит/символ\n")
        # f.write(f"Проверка декодирования: {'OK' if message == decoded else 'ERROR'}\n")
        f.close()

    print("\nРезультат добавлен в output_2.txt")
    return codebook, encoded

if __name__ == "__main__":
    shannon_main()