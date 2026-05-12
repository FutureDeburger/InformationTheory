

def hamming_encode(bits, m):

    n = 2 ** m - 1
    k = n - m
    if len(bits) != k:
        raise ValueError(f"Ожидалось {k} информационных битов, получено {len(bits)}")

    control_bits_positions = [2 ** i for i in range(m)]

    # Размещаем исходные биты в соответствии с размером кода
    code = [0] * n
    j = 0
    for i in range(1, n + 1):
        if i not in control_bits_positions:
            code[i - 1] = bits[j]
            j += 1

    # Вычисление проверочных битов
    for p in control_bits_positions:
        parity_sum = 0
        for i in range(1, n + 1):
            if i != p and (i & p) != 0:  # i-й бит участвует в проверке p
                parity_sum ^= code[i - 1]
        code[p - 1] = parity_sum  # проверочный бит

    return code


def code_rate(n, k):
    return k / n


def test_hamming():
    print("Код Хэмминга (7,4)")
    m7 = 3
    info = [1, 0, 1, 1]
    encoded = hamming_encode(info, m7)
    print("Информация:", info)
    print("Кодовое слово:", encoded)
    print(f"Скорость: {code_rate(7, 4):.3f}")

    print("\nКод Хэмминга (15,11)")
    info15 = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1]
    enc15 = hamming_encode(info15, 4)
    print("Информация:", info15)
    print("Кодовое слово:", enc15)
    print(f"Скорость: {code_rate(15, 11):.3f}")

    print("\nКод Хэмминга (31,26)")
    info31 = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0]
    enc31 = hamming_encode(info31, 5)
    print("Информация:", info31)
    print("Кодовое слово:", enc31)
    print(f"Скорость: {code_rate(31, 26):.3f}")


if __name__ == "__main__":
    test_hamming()