import matplotlib.pyplot as plt

# Definición de las regiones para Cohen-Sutherland
INSIDE = 0  # 0000
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8     # 1000

# Coordenadas del rectángulo de recorte
xmin, ymin = 1, 1
xmax, ymax = 4, 3

# Función para calcular el código de una coordenada (x, y)
def compute_out_code(x, y):
    code = INSIDE
    if x < xmin:
        code |= LEFT
    elif x > xmax:
        code |= RIGHT
    if y < ymin:
        code |= BOTTOM
    elif y > ymax:
        code |= TOP
    return code

# Algoritmo de Cohen-Sutherland
def cohen_sutherland_clip(x0, y0, x1, y1):
    outcode0 = compute_out_code(x0, y0)
    outcode1 = compute_out_code(x1, y1)
    accept = False

    while True:
        if outcode0 == 0 and outcode1 == 0:
            accept = True
            break
        elif outcode0 & outcode1 != 0:
            break
        else:
            x, y = 0.0, 0.0
            outcode_out = outcode0 if outcode0 != 0 else outcode1

            if outcode_out & TOP:
                x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0)
                y = ymax
            elif outcode_out & BOTTOM:
                x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0)
                y = ymin
            elif outcode_out & RIGHT:
                y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0)
                x = xmax
            elif outcode_out & LEFT:
                y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0)
                x = xmin

            if outcode_out == outcode0:
                x0, y0 = x, y
                outcode0 = compute_out_code(x0, y0)
            else:
                x1, y1 = x, y
                outcode1 = compute_out_code(x1, y1)

    if accept:
        return [(x0, y0), (x1, y1)]
    else:
        return None

# Líneas a recortar
# (inicial)x,y,(final)x,y
lines = [
    (0, 2, 5, 2),  # Línea cruzando horizontalmente
    (2, 0, 2, 4),  # Línea cruzando verticalmente
    (0, 0, 5, 3),  # Línea cruzando diagonalmente
    (3, 0, 6, 5)   # Otra línea diagonal fuera del área
]

# Graficar
fig, ax = plt.subplots()

# Dibujar el rectángulo de recorte
rect = plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, edgecolor='black', facecolor='lightgreen', linestyle='--')
ax.add_patch(rect)

# Dibujar las líneas originales y recortadas
for line in lines:
    x0, y0, x1, y1 = line
    clipped_line = cohen_sutherland_clip(x0, y0, x1, y1)
    
    # Línea original
    plt.plot([x0, x1], [y0, y1], 'r--')  # Línea original en rojo y discontinuo
    
    # Línea recortada
    if clipped_line:
        (cx0, cy0), (cx1, cy1) = clipped_line
        plt.plot([cx0, cx1], [cy0, cy1], 'b')  # Línea recortada en azul

# Ajustes finales
ax.set_xlim(0, 6)
ax.set_ylim(0, 5)
ax.set_aspect('equal')
plt.grid(True)
plt.show()
