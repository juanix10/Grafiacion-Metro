import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog

# Función Bresenham modificada
def bresenham(x0, y0, x1, y1):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    
    sx = 1 if x0 < x1 else -1  # Dirección en X
    sy = 1 if y0 < y1 else -1  # Dirección en Y
    
    err = dx - dy  # Error inicial
    
    points = []
    
    while True:
        points.append((x0, y0))  # Almacenar el punto actual
        
        if x0 == x1 and y0 == y1:
            break
        
        e2 = 2 * err  # Multiplicar el error por 2
        
        if e2 > -dy:
            err -= dy
            x0 += sx
        
        if e2 < dx:
            err += dx
            y0 += sy
    
    return points

# Función para solicitar los puntos y graficar
def solicitar_datos_y_graficar():
    # Crear ventana raíz
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    # Solicitar los valores al usuario
    x_inicial = int(simpledialog.askstring("Entrada", "Ingresa el valor de x0:"))
    y_inicial = int(simpledialog.askstring("Entrada", "Ingresa el valor de y0:"))
    x_final = int(simpledialog.askstring("Entrada", "Ingresa el valor de x1:"))
    y_final = int(simpledialog.askstring("Entrada", "Ingresa el valor de y1:"))

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

# Llamar a la función para solicitar datos y graficar
solicitar_datos_y_graficar()
