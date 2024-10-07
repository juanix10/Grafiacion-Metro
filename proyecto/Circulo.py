import matplotlib.pyplot as plt

# Lista de coordenadas X e Y proporcionadas en la imagen
x_coords = [5, 5, 5, 5, 11, -1, 11, -1, 6, 4, 6, 4, 11, -1, 11, -1, 7, 3, 7, 3, 11, -1, 11, -1, 8, 2, 8, 2, 10, 0, 10, 0, 9, 1, 9, 1, 10, 0, 10, 0]
y_coords = [14, 14, 2, 2, 8, 8, 8, 8, 14, 14, 2, 2, 9, 9, 7, 7, 14, 14, 2, 2, 10, 10, 6, 6, 13, 13, 3, 3, 11, 11, 5, 5, 13, 13, 3, 3, 12, 12, 4, 4]

# Crear el gráfico
plt.figure(figsize=(6, 6))  # Crear una figura cuadrada

# Graficar los puntos utilizando 'bo' para hacer que se vean como puntos azules
plt.plot(x_coords, y_coords, 'bo')

# Ajustar la escala de los ejes para que el gráfico sea simétrico
plt.gca().set_aspect('equal', adjustable='box')

# Título del gráfico
plt.title("Circunferencia usando el algoritmo de Bresenham")

# Mostrar el gráfico
plt.show()
