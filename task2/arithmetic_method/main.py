import math


def arithmetic_coding(symbols, probs, message):

    # Вычисление кумулятивных вероятностей q (левые границы)
    q = {}
    cumulative = 0.0

    pairs = list(zip(symbols, probs))
    pairs.sort(key=lambda x: x[1], reverse=True)

    for sym, p in pairs:
        q[sym] = cumulative
        cumulative += p

    # print("\nКумулятивные вероятности (левые границы):")
    # for sym, p in pairs:
    #     print(f"  {sym}: p={p}, q={q[sym]:.4f}, интервал [{q[sym]:.4f}, {q[sym] + p:.4f})")

    # Кодирование последовательности
    F = 0.0  # левая граница
    G = 1.0  # ширина интервала

    print(f"\nНачальный интервал: [{F}, {F + G})")

    for i, ch in enumerate(message):
        # Левая граница интервала символа
        q_ch = q[ch]
        # Ширина интервала символа
        p_ch = dict(pairs)[ch]

        # Новый интервал
        F_new = F + q_ch * G
        G_new = p_ch * G

        print(f"  {i + 1}. Символ '{ch}': q={q_ch:.4f}, p={p_ch:.4f}")
        print(f"     F = {F:.6f} + {q_ch:.4f} * {G:.6f} = {F_new:.6f}")
        print(f"     G = {p_ch:.4f} * {G:.6f} = {G_new:.6f}")
        print(f"     Интервал: [{F_new:.6f}, {F_new + G_new:.6f})")

        F, G = F_new, G_new

    # Формирование кодового слова
    midpoint = F + G / 2.0

    code_length = math.floor(-math.log2(G)) + 1

    # print(f"\nФинальный интервал: [{F:.10f}, {F + G:.10f})")
    # print(f"Ширина G = {G:.10f}")
    # print(f"Середина = {midpoint:.10f}")
    # print(f"Длина кода = floor(-log2({G:.10f})) + 1 = {code_length} бит")

    # Преобразуем середину в двоичную дробь
    encoded = fractional_to_binary(midpoint, code_length)

    return encoded, F, G, midpoint, code_length


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


def arithmetic_decode(encoded, symbols, probs, message_length):
    # Преобразуем двоичную дробь в число
    value = binary_to_fraction(encoded)

    print(f"\nДекодирование:")
    print(f"Закодированное значение: {value:.10f}")

    # Вычисляем кумулятивные вероятности
    pairs = list(zip(symbols, probs))
    pairs.sort(key=lambda x: x[1], reverse=True)

    q = {}
    cumulative = 0.0
    for sym, p in pairs:
        q[sym] = cumulative
        cumulative += p

    # Создаём список интервалов для поиска
    intervals = []
    for sym, p in pairs:
        intervals.append((sym, q[sym], q[sym] + p))

    # Декодирование
    decoded = []
    F = 0.0
    G = 1.0

    for _ in range(message_length):
        normalized = (value - F) / G

        found = False
        for sym, left, right in intervals:
            if left <= normalized < right:
                decoded.append(sym)
                print(f"  normalized={normalized:.6f} → символ '{sym}' (интервал [{left:.4f}, {right:.4f}))")

                p_sym = dict(pairs)[sym]
                F = F + left * G
                G = p_sym * G
                found = True
                break

        if not found:
            raise ValueError(f"Не удалось декодировать символ на позиции {len(decoded)}")

    return ''.join(decoded)


def binary_to_fraction(binary_string):
    value = 0.0
    for i, bit in enumerate(binary_string):
        if bit == '1':
            value += 2 ** (-(i + 1))
    return value


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


def arithmetic_main():
    """Главная функция для арифметического кодирования"""
    symbols, probs = read_alphabet("alphabet.txt")
    message = read_message("input.txt")

    encoded, final_F, final_G, midpoint, code_length = arithmetic_coding(symbols, probs, message)

    decoded = arithmetic_decode(encoded, symbols, probs, len(message))

    # entropy = -sum(p * math.log2(p) for p in probs if p > 0)
    # theoretical_min_length = entropy * len(message)

    with open("output_4.txt", "w", encoding="utf-8") as f:
        f.write("Арифметическое Кодирование\n")

        f.write(f"\nИсходное сообщение: {message}\n")
        f.write(f"Длина сообщения: {len(message)} символов\n")

        f.write("\nПараметры кодирования:\n")
        f.write(f"  Финальная левая граница F = {final_F:.10f}\n")
        f.write(f"  Финальная ширина G = {final_G:.10f}\n")
        f.write(f"  Середина интервала = {midpoint:.10f}\n")
        f.write(f"  Длина кода = {code_length} бит\n")

        f.write(f"\nЗакодированное сообщение: {encoded}\n")
        f.write(f"Декодированное сообщение: {decoded}\n")
        f.write(f"Длина кода: {len(encoded)} бит\n")

        # f.write(f"\nСтатистика:\n")
        # f.write(f"  Энтропия источника: {entropy:.4f} бит/символ\n")
        # f.write(f"  Теоретический минимум: {theoretical_min_length:.2f} бит\n")
        # f.write(f"  Фактическая длина: {len(encoded)} бит\n")
        # f.write(f"  Эффективность: {theoretical_min_length / len(encoded) * 100:.1f}%\n")
        # f.write(f"\nПроверка декодирования: {'OK' if message == decoded else 'ERROR'}\n")
        f.close()

    # print(f"\nЗакодированное сообщение: {encoded}")
    # print(f"Декодированное сообщение: {decoded}")
    # print(f"Длина кода: {len(encoded)} бит")
    print("\nРезультат добавлен в output_4.txt")

    return encoded, decoded


if __name__ == "__main__":
    arithmetic_main()