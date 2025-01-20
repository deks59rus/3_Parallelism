import numpy as np
import multiprocessing
import os

def read_matrices_from_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read().strip().split('\n\n')
        matrices = [np.array([[float(num) for num in line.split()] for line in matrix.splitlines()]) for matrix in content]
    return matrices

def write_element_to_file(file_path, matrix_index, row, col, value):
    with open(file_path, 'a') as f:
        f.write(f"{matrix_index} {row} {col} {value}\n")

def multiply_elements(args):
    A, B, matrix_index, row, col, output_file = args
    value = A[row, col] * B[row, col]
    write_element_to_file(output_file, matrix_index, row, col, value)

def main(matrix_a_file, matrix_b_file, output_file, num_processes):
    A_matrices = read_matrices_from_file(matrix_a_file)
    B_matrices = read_matrices_from_file(matrix_b_file)

    if len(A_matrices) != len(B_matrices):
        raise ValueError("Количество матриц в файлах должно совпадать.")

    if any(A.shape != B.shape for A, B in zip(A_matrices, B_matrices)):
        raise ValueError("Размеры соответствующих матриц должны совпадать.")

    if os.path.exists(output_file):
        os.remove(output_file)

    with multiprocessing.Pool(processes=num_processes) as pool:
        tasks = []
        for matrix_index, (A, B) in enumerate(zip(A_matrices, B_matrices)):
            for row in range(A.shape[0]):
                for col in range(A.shape[1]):
                    tasks.append((A, B, matrix_index, row, col, output_file))
        pool.map(multiply_elements, tasks)

if __name__ == "__main__":
    matrix_a_file = "matrix_a.txt"
    matrix_b_file = "matrix_b.txt"
    output_file = "result.txt"
    num_processes = 4

    main(matrix_a_file, matrix_b_file, output_file, num_processes)