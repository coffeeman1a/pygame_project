from opensimplex import OpenSimplex
import random

def generate_noise(width, height, scale):
    noise = OpenSimplex(random.randint(0, 100))
    noise_map = []

    for y in range(height):
        row = []
        for x in range(width):
            # Получение значения шума в диапазоне от -1 до 1
            sample_x = x / scale
            sample_y = y / scale
            value = noise.noise2(sample_x, sample_y)
            row.append(value)
        noise_map.append(row)

    return noise_map

# Пример использования
width = 100
height = 100
scale = 10

noise_map = generate_noise(width, height, scale)

# Вывод сгенерированного шума
for row in noise_map:
    print(row)
