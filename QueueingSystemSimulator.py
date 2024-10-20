import random
import math
import numpy as np
import matplotlib.pyplot as plt

# Задание №1: Генерация последовательностей случайных чисел
M = 1000
a_TZ = 39
a_TS = 39
b = 1
x0 = 1
n = 1000  # Количество случайных чисел


def generate_linear_sequence(a, b, M, x0, n, min_val, max_val):
    random_numbers = []
    for _ in range(n):
        x0 = (a * x0 + b) % M
        value = min_val + (max_val - min_val) * (x0 / M)
        random_numbers.append(value)
    return random_numbers


TZmin, TZmax = 4, 12  # Для входного потока заявок
TSmin, TSmax = 2, 8  # Для времени обработки заявок сервером

tz_sequence = generate_linear_sequence(a_TZ, b, M, x0, n, TZmin, TZmax)
ts_sequence = generate_linear_sequence(a_TS, b, M, x0, n, TSmin, TSmax)

# Задание №2: Определение времен прихода программ
print(f"Задание №2\n")
time_of_arrival = tz_sequence
print("Времена прихода программ в вычислительную систему:")
for i, time in enumerate(time_of_arrival, start=1):
    print(f"Программа {i}: {time:.2f} сек")


# Задание №3: Разработка программы для расчета времени нахождения программ в буфере
def calculate_time_in_buffer(tz_sequence, buffer_size):
    buffer = []
    time_in_buffer = []

    for tz in tz_sequence:
        if len(buffer) < buffer_size:
            buffer.append(tz)
        else:
            time_in_buffer.append(buffer.pop(0))
            buffer.append(tz)

    while buffer:
        time_in_buffer.append(buffer.pop(0))

    return time_in_buffer


# Задание №4: Определение времен нахождения в буфере
print(f"\nЗадание №4\n")
num_programs = [1, 2, 3, 4, 5]
for num in num_programs:
    total_time = 0
    time_in_buffer = calculate_time_in_buffer(tz_sequence, num)
    print(f'Времена нахождения в буфере для {num} программ: {time_in_buffer}')
    total_time = sum(time_in_buffer)
    print(f'Общее время нахождения в буфере для {num} программ: {total_time:.2f} секунд')

# Задание №5: Расчет вероятностей нахождения в буфере
print(f"\nЗадание №5")
print(f"Для буфера неограниченной вместимости\n")


def calculate_probability_in_buffer(tz_sequence, buffer_size, num_programs):
    time_in_buffer = calculate_time_in_buffer(tz_sequence, buffer_size)
    total_programs = len(tz_sequence)
    count = 0
    for i in range(len(tz_sequence) - num_programs + 1):
        if all(tz_sequence[i + j] in time_in_buffer for j in range(num_programs)):
            count += 1
    probability = count / (total_programs - num_programs + 1)
    return probability


for num in num_programs:
    probability = calculate_probability_in_buffer(tz_sequence, num, num)
    print(f'Вероятность нахождения {num} программ в буфере: {probability:.2f}')

print(f"\nДля буфера с ограниченной вместимостью\n")

def buffer_probabilities(tz_sequence, buffer_size):
    buffer = []  # Буфер
    time_in_buffer_count = [0] * (buffer_size + 1)

    for arrival_time in tz_sequence:
        while buffer and buffer[0] <= arrival_time:
            time_in_buffer_count[len(buffer)] += 1
            buffer.pop(0)

        if len(buffer) < buffer_size:
            buffer.append(arrival_time)
        else:
            time_in_buffer_count[buffer_size] += 1

    total_arrivals = len(tz_sequence)
    probabilities = [count / total_arrivals for count in time_in_buffer_count]

    return probabilities

buffer_size = 5

probabilities = buffer_probabilities(tz_sequence, buffer_size)
print("Вероятности нахождения в буфере:")
for i, probability in enumerate(probabilities):
    print(f"{i} программ: {probability * 100:.5f}%")


# Задание №6: Генерация последовательностей по экспоненциальным законам
lambda_value = 1 / 3  # Параметр lambda для входного потока
mu_value = 1 / 4  # Параметр mu для времени обработки

exponential_input = [-math.log(1 - random.random()) / lambda_value for _ in range(n)]
exponential_processing = [-math.log(1 - random.random()) / mu_value for _ in range(n)]

# Задание №7: Расчет времени нахождения программ в буфере для экспоненциальных законов
print(f"\nЗадание №7\n")
for num in num_programs:
    total_time = 0
    time_in_buffer = calculate_time_in_buffer(exponential_input, num)
    print(f'Времена нахождения в буфере для {num} программ (экспоненциальное): {time_in_buffer}')
    total_time = sum(time_in_buffer)
    print(f'Общее время нахождения в буфере для {num} программ: {total_time:.2f} секунд')
