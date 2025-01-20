import numpy as np
import concurrent.futures
import threading
import time

class MatrixMultiplier:
    def __init__(self, size, num_matrices, output_file):
        self.size = size
        self.num_matrices = num_matrices
        self.results = []
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.output_file = output_file

    def generate_matrix(self):
        return np.random.randint(1, 10, size=(self.size, self.size))

    def multiply_matrices(self, A, B, index):
        value = A @ B  # Используем матричное умножение
        with self.lock:
            self.results.append((index, value))

    def write_results_to_file(self):
        with open(self.output_file, 'w') as f:
            for index, result in self.results:
                f.write(f"Матрица {index}:\n{result}\n\n")

    def run(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for index in range(self.num_matrices):
                A = self.generate_matrix()
                B = self.generate_matrix()
                executor.submit(self.multiply_matrices, A, B, index)

                if self.stop_event.is_set():
                    print("Процесс перемножения остановлен.")
                    break

                time.sleep(5)  # Задержка для демонстрации асинхронности

    def stop(self):
        self.stop_event.set()

if __name__ == "__main__":
    size = 3  # Размерность матриц
    num_matrices = 10  # Количество матриц
    output_file = "results.txt"  # Файл для сохранения результатов

    multiplier = MatrixMultiplier(size, num_matrices, output_file)

    try:
        multiplier_thread = threading.Thread(target=multiplier.run)
        multiplier_thread.start()

        # Остановка через 5 секунд (для тестирования)
        time.sleep(5)
        multiplier.stop()
    finally:
        multiplier_thread.join()

    # Запись результатов в файл
    multiplier.write_results_to_file()
    print(f"Результаты перемножения сохранены в файл: {output_file}")
