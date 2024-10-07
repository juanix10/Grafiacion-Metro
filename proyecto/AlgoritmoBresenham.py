import matplotlib.pyplot as plt

def bresenham(x1, y1, x2, y2):
    # Calcular las diferencias
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    
    # Determinar la dirección de incremento
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    # Inicializar el parámetro de decisión
    err = dx - dy

    # Crear una lista para almacenar los puntos de la línea
    points = []

    while True:
        # Añadir el punto actual a la lista
        points.append((x1, y1))
        
        # Si el punto inicial es igual al punto final, terminar el algoritmo
        if x1 == x2 and y1 == y2:
            break
        
        # Calcular el doble del error
        e2 = 2 * err
        
        # Ajustar el error y mover en x o y según corresponda
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

    return points

def plot_line(points):
    # Separar las coordenadas x e y
    x_coords, y_coords = zip(*points)
    
    # Crear un gráfico donde se simulen los píxeles
    plt.figure(figsize=(5, 5))
    plt.plot(x_coords, y_coords, marker='o', color='black', linestyle='None')
    plt.grid(True)
    plt.xticks(range(min(x_coords) - 1, max(x_coords) + 2))
    plt.yticks(range(min(y_coords) - 1, max(y_coords) + 2))
    plt.gca().invert_yaxis()  # Invertir el eje y para simular coordenadas de píxeles
    plt.show()

# Coordenadas del punto inicial y final
x1, y1 = 2, 3
x2, y2 = 10, 7

# Trazar la línea usando el algoritmo de Bresenham
line_points = bresenham(x1, y1, x2, y2)

# Mostrar la línea en una cuadrícula
plot_line(line_points)
