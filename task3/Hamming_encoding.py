import math


def Hamming_encoding(word):

    m = math.ceil(math.log((len(word) + 1 + math.log(len(word))), 2)) # Вычисление количества проверочных бит
    n = 2 ** m - 1
    k = n - m
    if m != (n - k):
        raise ValueError(f"Неверно вычислено m (число проверочных бит): {m}")

    control_bits_positions = [2 ** i for i in range(m)] # позиции проверочных бит

    # Размещаем исходные биты в соответствии с размером кода
    code = [0] * n
    word_index = 0
    for position in range(1, n + 1):
        if position not in control_bits_positions:
            code[position - 1] = word[word_index]
            word_index += 1

    # Вычисление проверочных битов
    for position in control_bits_positions:
        parity_sum = 0
        for i in range(1, n + 1):
            if i != position and (i & position) != 0:  # i-й бит участвует в проверке p
                parity_sum ^= code[i - 1]
        code[position - 1] = parity_sum  # проверочный бит

    return code


def Hamming_code_rate(word):
    m = math.ceil(math.log((len(word) + 1 + math.log(len(word))), 2))
    n = 2 ** m - 1
    k = n - m
    return k / n


def build_H(word, hamm_code):
    m = len(hamm_code) - len(word)
    n = len(hamm_code)
    H = []

    for num in range(1, n + 1):
        binary = []
        for i in range(m - 1, -1, -1):
            binary.append((num >> i) & 1)
        H.append(binary)

    H_matrix = list(zip(*H))
    return H_matrix


def calculate_syndrome(word, hamm_code):
    m = len(hamm_code) - len(word)
    n = len(hamm_code)
    H = build_H(word, hamm_code)
    syndrome = []

    for row in H:
        parity = 0
        for i in range(len(H[0])):
            parity ^= (row[i] & hamm_code[i])
        syndrome.append(parity)

    return syndrome


def conversion_from_bin_to_dec(syndrome):
    error_pos = 0
    for i, bit in enumerate(reversed(syndrome)):
        error_pos += bit * (2 ** i)
    return error_pos


def fixer_error_in_hamm_code(word, hamm_code):
    syndrome = calculate_syndrome(word, hamm_code)
    dec_syndrome = conversion_from_bin_to_dec(syndrome)

    fixed_code = hamm_code.copy()
    if dec_syndrome != 0:
        fixed_code[dec_syndrome - 1] ^= 1

    return fixed_code


if __name__ == "__main__":

    print("Код Хэмминга (7, 4)")
    word1 = [1, 0, 1, 1]
    hamm_code1 = Hamming_encoding(word1)
    print(f"Исходное слово: {word1}")
    print(f"Код Хэмминга: {hamm_code1}")
    print(f"Скорость кода Хэмминга: {round(Hamming_code_rate(word1), 3)}")

    print("\nКод Хэмминга (15, 11)")
    word2 = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1]
    hamm_code2 = Hamming_encoding(word2)
    print(f"Исходное слово: {word2}")
    print(f"Код Хэмминга: {hamm_code2}")
    print(f"Скорость кода Хэмминга: {round(Hamming_code_rate(word2), 3)}")

    print("\nКод Хэмминга (31, 26)")
    word3 = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0]
    hamm_code3 = Hamming_encoding(word3)
    print(f"Исходное слово: {word3}")
    print(f"Код Хэмминга: {hamm_code3}")
    print(f"Скорость кода Хэмминга: {round(Hamming_code_rate(word3), 3)}")


    # Матрицы H
    # for row in build_H(word1, hamm_code1):
    #     print(row)
    #
    # for row in build_H(word2, hamm_code2):
    #     print(row)
    #
    # for row in build_H(word3, hamm_code3):
    #     print(row)


    # syndrome1 = calculate_syndrome(word1, hamm_code1)
    # print(syndrome1)
    # rec_syndrome1 = conversion_from_bin_to_dec(syndrome1)
    # print(rec_syndrome1)


    # Проверка декодирования с ошибкой
    # f1 = fixer_error_in_hamm_code(word1,  [0, 1, 1, 1, 0, 1, 0])
    # print(f1)
    #
    # f2 = fixer_error_in_hamm_code(word2, [1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0])
    # print(f2)