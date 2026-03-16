import math


def read_file(filename):
    matrix = []
    with open(filename, 'r') as f:
        for line in f:
            row = list(map(float, line.strip().split()))
            matrix.append(row)
    return matrix

def write_file(filename, res_list):
    with open(filename, 'w') as f:
        for line in res_list:
            f.write(str(line) + '\n')

def find_entropy_X(matrix):
    entropy = 0
    for row in matrix:
        p = sum(row)
        if p > 0:
            entropy += -p * math.log2(p)
    return entropy

def find_entropy_Y(matrix):
    entropy = 0
    for j in range(len(matrix[0])):
        p = 0
        for i in range(len(matrix)):
            p += matrix[i][j]
        if p > 0:
            entropy += -p * math.log2(p)
    return entropy

def find_joint_entropy(matrix):
    entropy = 0
    for row in matrix:
        for p in row:
            if p > 0:
                entropy += -p * math.log2(p)
    return entropy

def find_conditional_entropy_XY(matrix):
    return find_joint_entropy(matrix) - find_entropy_Y(matrix)

def find_conditional_entropy_YX(matrix):
    return find_joint_entropy(matrix) - find_entropy_X(matrix)

def find_mutual_information(matrix):
    return find_entropy_X(matrix) - find_conditional_entropy_XY(matrix)

if __name__ == '__main__':

    input_matrix = read_file('input.txt')

    entropy_x = find_entropy_X(input_matrix)
    str_entropy_x = f'H(X) = {entropy_x}'
    print(str_entropy_x)
    # print(f'H(X) = {entropy_x}')

    entropy_y = find_entropy_Y(input_matrix)
    str_entropy_y = f'H(Y) = {entropy_y}'
    print(str_entropy_y)
    # print(f'H(Y) = {entropy_y}')

    conditional_entropy_XY = find_conditional_entropy_XY(input_matrix)
    str_conditional_entropy_XY = f'H(X|Y) = {conditional_entropy_XY}'
    print(str_conditional_entropy_XY)
    # print(f'H(X|Y) = {conditional_entropy_XY}')

    conditional_entropy_YX = find_conditional_entropy_YX(input_matrix)
    str_conditional_entropy_YX = f'H(Y|X) = {conditional_entropy_YX}'
    print(str_conditional_entropy_YX)
    # print(f'H(Y|X) = {conditional_entropy_YX}')

    joint_entropy = find_joint_entropy(input_matrix)
    str_joint_entropy = f'H(X,Y) = {joint_entropy}'
    print(str_joint_entropy)
    # print(f'H(X,Y) = {joint_entropy}')

    mutual_information = find_mutual_information(input_matrix)
    str_mutual_information = f'I(X,Y) = {mutual_information}'
    print(str_mutual_information)
    # print(f'I(X,Y) = {mutual_information}')


    result_list = [str_entropy_x, str_entropy_y, str_conditional_entropy_XY, str_conditional_entropy_YX, str_joint_entropy, str_mutual_information]
    print(result_list)


    # write_file('output.txt', result_list)