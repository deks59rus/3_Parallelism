import numpy as np
import concurrent.futures
import threading

class MatrixMultiplier:
    def __init__(self, size, num_matrices, output_file, num_threads):
        self.size = size
        self.num_matrices = num_matrices
        self.results = []
        self.lock = threading.Lock()
        self.output_file = output_file
        self.num_threads = num_threads

    def generate_matrix(self):
        return np.random.randint(1, 10, size=(self.size, self.size))

    def multiply_matrices(self, A, B, index):
        value = A @ B  # Используем матричное умножение
        with self.lock:
            self.results.append((index, value))
            # Печатаем промежуточный результат в консоль
            print(f"Поток {threading.current_thread().name} перемножает матрицы {index}:\n{value}\n")

    def write_results_to_file(self):
        with open(self.output_file, 'w') as f:
            for index, result in self.results:
                f.write(f"Матрица {index}:\n{result}\n\n")

    def run(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            futures = []
            for index in range(self.num_matrices):
                A = self.generate_matrix()
                B = self.generate_matrix()
                futures.append(executor.submit(self.multiply_matrices, A, B, index))

            # Ждем завершения всех задач
            concurrent.futures.wait(futures)

if __name__ == "__main__":
    size = 3  # Размерность матриц
    num_matrices = 1000  # Количество матриц
    output_file = "results.txt"  # Файл для сохранения результатов
    num_threads = 4  # Количество потоков

    multiplier = MatrixMultiplier(size, num_matrices, output_file, num_threads)
    multiplier.run()

    # Запись результатов в файл
    multiplier.write_results_to_file()
    print(f"Результаты перемножения сохранены в файл: {output_file}")
