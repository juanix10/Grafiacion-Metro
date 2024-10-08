import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Definición de las regiones para Cohen-Sutherland
INSIDE = 0  # 0000
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8     # 1000

# Coordenadas del rectángulo de recorte (actualizadas a 0, 0 y 100, 100)
xmin, ymin = 0, 0
xmax, ymax = 100, 100

# Líneas definidas por el usuario
lines = []

# Variables para almacenar el estado de clics
clicks = []

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

# Función para dibujar las líneas
def dibujar_lineas(ax, lineas, color='r--', recortadas=False):
    for line in lineas:
        x0, y0, x1, y1 = line
        if recortadas:
            clipped_line = cohen_sutherland_clip(x0, y0, x1, y1)
            if clipped_line:
                (cx0, cy0), (cx1, cy1) = clipped_line
                ax.plot([cx0, cx1], [cy0, cy1], 'b')  # Línea recortada en azul
        else:
            ax.plot([x0, x1], [y0, y1], color)  # Línea original en rojo discontinuo

# Función para ejecutar el recorte
def recortar(event):
    ax.clear()
    # Dibujar el rectángulo de recorte
    rect = plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, edgecolor='black', facecolor='lightgreen', linestyle='--')
    ax.add_patch(rect)
    
    # Dibujar las líneas recortadas
    dibujar_lineas(ax, lines, recortadas=True)
    
    plt.draw()

# Función para reiniciar
def reiniciar(event):
    global lines
    lines = []  # Borrar todas las líneas
    ax.clear()  # Limpiar el gráfico
    
    # Redibujar el rectángulo de recorte
    rect = plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, edgecolor='black', facecolor='lightgreen', linestyle='--')
    ax.add_patch(rect)
    
    plt.draw()

# Función para manejar los clics del usuario
def on_click(event):
    # Guardar las coordenadas de los clics
    if event.inaxes is not None:
        clicks.append((event.xdata, event.ydata))
        if len(clicks) == 2:
            x0, y0 = clicks[0]
            x1, y1 = clicks[1]
            lines.append((x0, y0, x1, y1))  # Añadir nueva línea
            clicks.clear()  # Limpiar los clics
            ax.clear()  # Limpiar el gráfico antes de redibujar

            # Redibujar el rectángulo y las líneas
            rect = plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, edgecolor='black', facecolor='lightgreen', linestyle='--')
            ax.add_patch(rect)
            dibujar_lineas(ax, lines)  # Dibujar todas las líneas
            plt.draw()

# Graficar
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)

# Dibujar el rectángulo de recorte
rect = plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, edgecolor='black', facecolor='lightgreen', linestyle='--')
ax.add_patch(rect)

# Crear el botón "Recortar"
ax_recortar = plt.axes([0.7, 0.05, 0.1, 0.075])
btn_recortar = Button(ax_recortar, 'Recortar')

# Crear el botón "Reiniciar"
ax_reiniciar = plt.axes([0.8, 0.05, 0.1, 0.075])
btn_reiniciar = Button(ax_reiniciar, 'Reiniciar')

# Vincular el evento del botón a la función de recorte y reinicio
btn_recortar.on_clicked(recortar)
btn_reiniciar.on_clicked(reiniciar)

# Vincular el evento de clic del usuario a la función on_click
cid = fig.canvas.mpl_connect('button_press_event', on_click)

# Configuración final
ax.set_xlim(-50, 150)  # Mostrar áreas negativas y mayores a 100
ax.set_ylim(-50, 150)  # Mostrar áreas negativas y mayores a 100
ax.set_aspect('equal')
plt.grid(True)
plt.show()
