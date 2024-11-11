import numpy as np
from PIL import Image


def grayscale_image(image_array, weights):
    if image_array.shape[2] != len(weights):
        raise ValueError("Количество каналов в изображении не соответствует длине вектора весов.")

    gray_image = np.dot(image_array, weights)

    return gray_image


image_path = 'images.jpeg'
image = Image.open(image_path).convert('RGB')
image_array = np.array(image)

weights = np.array([0.299, 0.587, 0.114])

gray_image = grayscale_image(image_array, weights)

print("Исходное изображение:")
print(image_array)
print("\nПреобразованное изображение в оттенки серого:")
print(gray_image)