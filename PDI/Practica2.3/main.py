import numpy as np
import cv2
import pandas as pd

# Lectura de la imagen de entrada
imagen_original = cv2.imread('peppers.png', 0)

# Tamaño de la matriz imagen_gris
filas, columnas = imagen_original.shape

# Tamaño del bloque para la DCT
tam_bloque = 8

# Restamos 128 a toda la matriz
im_rest = imagen_original - 128

# Aplicamos la dct
im_dct = cv2.dct(np.float32(im_rest))

# Creamos nuestra matriz cuantificadora
cuantificador = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                          [12, 12, 14, 19, 26, 58, 60, 55],
                          [14, 13, 16, 24, 40, 57, 69, 56],
                          [14, 17, 22, 29, 51, 87, 80, 62],
                          [18, 22, 37, 56, 68, 109, 103, 77],
                          [24, 35, 55, 64, 81, 104, 113, 92],
                          [49, 64, 78, 87, 103, 121, 120, 101],
                          [72, 92, 95, 98, 112, 100, 103, 99]])

# Cálculo del número de bloques de 8x8 en cada dirección
num_bloques_filas = filas // tam_bloque
num_bloques_columnas = columnas // tam_bloque

# Creación de la tabla de categorías
dc_table = pd.DataFrame({'Category': range(15),
                         'Base Code': ['010', '011', '100', '00', '101', '110', '1110', '11110', '111110', '1111110',
                                       '11111110', '111111110', '1111111110', '11111111110', '111111111110'],
                         'Length': [3, 4, 5, 5, 7, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26]})
# Aquí se omite la creación de la tabla ac_table por brevedad, pero se seguiría un procedimiento similar al de dc_table
# Recorremos la matriz en bloque de 8x8
for i in range(0, height, 8):
    for j in range(0, width, 8):
        # Obtenemos el bloque actual
        bloque = imagen[i:i+8, j:j+8]
        # Aplicamos la DCT a cada bloque
        dct_bloque = cv2.dct(np.float32(bloque))
        # Cuantificamos el bloque usando la matriz de cuantificación
        cuantificado_bloque = np.round(dct_bloque / q)
        # Añadimos el bloque cuantificado a la matriz resultante
        imagen_cuantificada[i:i+8, j:j+8] = cuantificado_bloque
