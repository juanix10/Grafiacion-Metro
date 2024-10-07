import matplotlib.pyplot as plt

# Función Bresenham modificada
def bresenham(x0, y0, x1, y1):
    # Calcular las diferencias
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    
    # Inicializar las variables
    sx = 1 if x0 < x1 else -1  # Dirección en X
    sy = 1 if y0 < y1 else -1  # Dirección en Y
    
    err = dx - dy  # Error inicial
    
    # Lista para almacenar los puntos de la línea
    points = []
    
    while True:
        points.append((x0, y0))  # Almacenar el punto actual
        
        # Si se ha llegado al punto final, se termina
        if x0 == x1 and y0 == y1:
            break
        
        e2 = 2 * err  # Multiplicar el error por 2
        
        if e2 > -dy:  # Ajustar error y mover en X
            err -= dy
            x0 += sx
        
        if e2 < dx:  # Ajustar error y mover en Y
            err += dx
            y0 += sy
    
    return points

# Definir los puntos de la línea
x_inicial, y_inicial = 2, 2
x_final, y_final = 10, 6

# Obtener la línea usando Bresenham
linea = bresenham(x_inicial, y_inicial, x_final, y_final)

# Extraer los puntos X e Y para graficar
x_vals, y_vals = zip(*linea)

# Graficar los puntos generados con anotaciones
plt.figure(figsize=(6,6))
plt.scatter(x_vals, y_vals, color='blue', s=100)  # Graficar los puntos individuales
plt.plot(x_vals, y_vals, color='lightblue', linestyle='--')  # Línea punteada que conecta los puntos

# Añadir etiquetas a cada punto
for x, y in linea:
    plt.text(x, y, f"({x},{y})", fontsize=12, ha='right')

plt.title("Línea usando el algoritmo de Bresenham")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.show()
