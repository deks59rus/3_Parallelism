import numpy as np
import concurrent.futures
import threading
import logging
import os
from datetime import datetime


# Функция для создания уникального имени лог-файла
def get_log_file_name():
    log_files = [f for f in os.listdir('.') if f.startswith('matrix_multiplication_') and f.endswith('.log')]
    log_files.sort()  # Сортируем файлы по имени (по времени создания)

    # Если больше 5 лог-файлов, удаляем самый старый
    if len(log_files) >= 5:
        os.remove(log_files[0])

    # Создаем новый лог-файл с текущей датой и временем
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"matrix_multiplication_{timestamp}.log"


# Настройка логирования
log_file_name = get_log_file_name()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename=log_file_name,
                    filemode='w')


class MatrixMultiplier:
    def __init__(self, size, num_matrices, output_file):
        self.size = size
        self.num_matrices = num_matrices
        self.results = []
        self.lock = threading.Lock()
        self.output_file = output_file
        self.num_threads = os.cpu_count()  # Автоматически определяем количество потоков

    def generate_matrix(self):
        return np.random.randint(1, 10, size=(self.size, self.size))

    def multiply_matrices(self, A, B, index):
        value = A @ B  # Используем матричное умножение
        with self.lock:
            self.results.append((index, value))
            # Логируем промежуточный результат
            logging.info(f"Поток {threading.current_thread().name} перемножает матрицы {index}:\n{value.tolist()}\n")

    def format_matrix(self, matrix):
        """Форматирует матрицу в виде строки для красивого отображения."""
        return '\n'.join([' '.join([f"{num:2}" for num in row]) for row in matrix])

    def write_results_to_file(self):
        with open(self.output_file, 'w') as f:
            for index, result in self.results:
                f.write(f"Матрица {index}:\n{self.format_matrix(result)}\n\n")

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
    size = 6  # Размерность матриц
    num_matrices = 100  # Количество матриц (уменьшено для примера, можно увеличить)
    output_file = "large_matrix_results.txt"  # Файл для сохранения результатов

    multiplier = MatrixMultiplier(size, num_matrices, output_file)
    multiplier.run()

    # Запись результатов в файл
    multiplier.write_results_to_file()
    logging.info(f"Результаты перемножения сохранены в файл: {output_file}")
